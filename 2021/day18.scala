import scala.io.Source
import scala.collection.mutable

import scala.util.control.Breaks._

object Day18 {

  class Leaf {
    var x: Int = _
    override def toString(): String = {
      x.toString
    }
  }

  class Node {
    var left: Either[Node, Leaf] = _
    var right: Either[Node, Leaf] = _
    override def toString(): String = {
      val l = left match {
        case Left(x)  => x
        case Right(x) => x
      }
      val r = right match {
        case Left(x)  => x
        case Right(x) => x
      }
      "[" + l + "," + r + "]"
    }
  }

  type Tree = Either[Node, Leaf]

  object Leaf {
    def apply(x: Int): Leaf = {
      var l = new Leaf
      l.x = x
      l
    }
  }

  object Node {
    def apply(left: Tree, right: Tree): Node = {
      var n = new Node
      n.left = left
      n.right = right
      n
    }
  }

  case class ParseResult(n: Node, parents: mutable.Map[Tree, Node])

  def add(p1: ParseResult, p2: ParseResult): ParseResult = {
    if (p1.n == null) {
      reduce(p2)
      p2
    } else {
      val n = Node(Left(p1.n), Left(p2.n))
      val parents = mutable.Map() ++ p1.parents ++ p2.parents

      parents(Left(p1.n)) = n
      parents(Left(p2.n)) = n

      val p = ParseResult(n, parents)
      reduce(p)
      p
    }
  }

  // Return parsed tree and parent mapping
  def parse(s: String): ParseResult = {
    // tokenize
    val ts = s.filter(_ != ',')

    val stack = mutable.Stack[Any]()

    val parents = mutable.Map[Tree, Node]()

    for (t <- ts) {
      if (t != ']') {
        stack.push(t)
      } else {
        val right: Tree = stack.pop() match {
          case n: Node => Left(n)
          case c: Char => Right(Leaf(c.asDigit))
          case _       => throw new Exception("Expected Node or Char")
        }
        val left: Tree = stack.pop() match {
          case n: Node => Left(n)
          case c: Char => Right(Leaf(c.asDigit))
          case _       => throw new Exception("Expected Node or Char")
        }
        // remove [
        stack.pop()
        val n = Node(left, right)
        parents(left) = n
        parents(right) = n
        stack.push(n)
      }
    }

    assert(stack.size == 1, "Incorrect string input")

    ParseResult(stack.pop().asInstanceOf[Node], parents)
  }

  // Returns inorder sequence of leafs and their depths
  def inorder(n: Node, depth: Int = 0): Seq[(Leaf, Int)] = {
    assert(depth < 5, f"Incorrect depth=$depth")
    val left = n.left match {
      case Left(n2) => inorder(n2, depth + 1)
      case Right(l) => {
        Seq((l, depth))
      }
    }
    val right = n.right match {
      case Left(n2) => inorder(n2, depth + 1)
      case Right(l) => {
        Seq((l, depth))
      }
    }
    left ++ right
  }

  def explode(
      n: Node,
      parents: mutable.Map[Tree, Node]
  ): Boolean = {
    val leafs = inorder(n)

    leafs.zipWithIndex.find(p => p._1._2 == 4) match {
      case Some(p) => {
        val Tuple2(Tuple2(l, d), idx) = p
        // Now, previous node is at idx-1
        // The pair to explode at idx and idx+1
        // The next node is at idx+2

        val Tuple2(l2, d2) = leafs(idx + 1)

        val leaf = Right(l)

        // Fix the parent
        val parent = Left(parents(leaf))

        assert(
          parent == Left(parents(Right(l2))),
          "siblings must share the same parent"
        )
        assert(d == d2, f"Depths differ $d vs $d2")

        val parentParent = parents(parent)
        val zero = Right(Leaf(0))
        // See if the parent-to-remove is left or right child
        if (parentParent.left == parent) {
          parentParent.left = zero
        } else {
          assert(parentParent.right == parent)
          parentParent.right = zero
        }

        parents(zero) = parentParent

        // Remove old pair and parent
        parents.remove(leaf)
        parents.remove(Right(l2))
        parents.remove(parent)

        // Fix the left
        if (idx - 1 >= 0) {
          val Tuple2(left, _) = leafs(idx - 1)
          left.x += l.x
        }

        // Fix the right
        if (idx + 2 < leafs.size) {
          val Tuple2(right, _) = leafs(idx + 2)
          right.x += l2.x
        }

        true
      }
      case _ => false
    }
  }

  def split(
      n: Node,
      parents: mutable.Map[Tree, Node]
  ): Boolean = {
    val leafs = inorder(n)

    leafs.find(p => p._1.x > 9) match {
      case Some(p) => {
        val Tuple2(l, _) = p

        val leaf = Right(l)
        val parent = parents(leaf)

        val left = Right(Leaf(l.x / 2))
        val right = Right(Leaf(l.x - l.x / 2))
        val n2 = Node(left, right)
        val newNode = Left(n2)

        parents(left) = n2
        parents(right) = n2

        // See if the leaf is left or right child
        if (parent.left == leaf) {
          parent.left = newNode
        } else {
          assert(parent.right == leaf)
          parent.right = newNode
        }

        parents(newNode) = parent

        // Remove the old leaf
        parents.remove(leaf)

        true
      }
      case _ => false
    }
  }

  def reduce(p: ParseResult): Unit = {
    while (explode(p.n, p.parents) || split(p.n, p.parents)) {}
  }

  def magnitude(n: Node): Int = {
    val left = n.left match {
      case Left(n2) => magnitude(n2)
      case Right(l) => l.x
    }
    val right = n.right match {
      case Left(n2) => magnitude(n2)
      case Right(l) => l.x
    }
    3 * left + 2 * right
  }

  def combinationTwo(s: String): Seq[String] = {
    val ret = mutable.Buffer[String]()
    val ss = s.split("\n")
    for (i <- 0 to ss.size - 1) {
      for (j <- 0 to ss.size - 1) {
        if (i != j) {
          ret.append(ss(i) + "\n" + ss(j))
        }
      }
    }
    ret.toSeq
  }

  def main(args: Array[String]): Unit = {
    val s =
      Source
        .fromFile("day18.txt")
        .mkString

    val p = s.split("\n").map(parse).foldLeft(ParseResult(null, null))(add)

    // Answer 1: 3665
    println(magnitude(p.n))

    var maxMagnitude = Int.MinValue

    for (s2 <- combinationTwo(s)) {
      val p = s2.split("\n").map(parse).foldLeft(ParseResult(null, null))(add)
      maxMagnitude = Math.max(maxMagnitude, magnitude(p.n))
    }

    // Answer 2: 4775
    println(maxMagnitude)
  }
}
