import scala.io.Source
import scala.collection.mutable.Map
import scala.collection.mutable.Stack

object Day10 {

  val closeToOpen = Map(
    ')' -> '(',
    ']' -> '[',
    '}' -> '{',
    '>' -> '<'
  )
  val open = closeToOpen.values.toVector

  def parseNext(
      c: Char,
      stack: Stack[Char],
      illegalCount: Map[Char, Int]
  ): Boolean = {
    if (open.contains(c)) {
      stack.push(c)
      true
    } else {
      if (closeToOpen(c) != stack.pop()) {
        illegalCount(c) += 1
        false
      } else {
        true
      }
    }
  }

  // Return the stack if the line is incomplete (i.e. not corrupted)
  def parse(
      line: Vector[Char],
      illegalCount: Map[Char, Int]
  ): Option[Stack[Char]] = {
    val stack = Stack[Char]()
    val noParseErrors = line.forall(c => parseNext(c, stack, illegalCount))
    if (noParseErrors) {
      Some(stack)
    } else {
      None
    }
  }

  def main(args: Array[String]): Unit = {
    val inputs =
      Source
        .fromFile("day10.txt")
        .mkString
        .split("\n")
        .map(_.toVector)

    // Part 1

    val illegalCount = Map[Char, Int]().withDefaultValue(0)

    inputs.foreach(line => parse(line, illegalCount))

    val points = Map(
      ')' -> 3,
      ']' -> 57,
      '}' -> 1197,
      '>' -> 25137
    )

    // Answer 1: 442131
    println(illegalCount.map((p => p._2 * points(p._1))).sum)

    // Part 2

    val points2 = Map(
      '(' -> 1,
      '[' -> 2,
      '{' -> 3,
      '<' -> 4
    )

    val scores = inputs
      .map(line => {
        // We do not care about illegal counts anymore
        parse(line, illegalCount) match {
          case Some(stack) => {
            stack.foldLeft(0L)((acc, c) => acc * 5 + points2(c))
          }
          case None => -1
        }
      })
      .filter(_ > -1)
      .sorted
      .toVector

    // Answer 2: 3646451424
    println(scores(scores.size / 2))
  }

}
