import scala.io.Source
import scala.collection.mutable.HashMap


object Day5 {

  class Line(val p1: (Int, Int), val p2: (Int, Int)) {

    override def toString(): String = {
      f"$p1 to $p2"
    }

    def isHorizontal(): Boolean = {
      p1._2 == p2._2
    }

    def isVertical(): Boolean = {
      p1._1 == p2._1
    }

    def generatePoints(): Seq[(Int, Int)] = {
      // Could probably simplify this with a single implementation
      if (isHorizontal) {
        val x1 = p1._1.min(p2._1)
        val x2 = p1._1.max(p2._1)
        val y = p1._2
        (x1 to x2).map(x => (x, y))
      } else if (isVertical) {
        val y1 = p1._2.min(p2._2)
        val y2 = p1._2.max(p2._2)
        val x = p1._1
        (y1 to y2).map(y => (x, y))
      } else {
        // Diagonal at 45 degrees

        val diffX = p1._1 - p2._1
        val diffY = p1._2 - p2._2

        val xRange = if (diffX > 0) {
          (0 to diffX)
        } else {
          (0 to diffX by -1)
        }

        val yRange = if (diffY > 0) {
          (0 to diffY)
        } else {
          (0 to diffY by -1)
        }

        xRange zip yRange map { case (dx, dy) => (p2._1 + dx, p2._2 + dy) } 
      }
    }

  }

  object Line {
    def parseLine(s: String): Line = {
      val arr = s.split(" -> ").map(_.split(",").map(_.toInt))
      new Line( (arr(0)(0), arr(0)(1)), (arr(1)(0), arr(1)(1)) )
    }
  }

  def main(args: Array[String]): Unit = {
    val s = """0,9 -> 5,9
8,0 -> 0,8
9,4 -> 3,4
2,2 -> 2,1
7,0 -> 7,4
6,4 -> 2,0
0,9 -> 2,9
3,4 -> 1,4
0,0 -> 8,8
5,5 -> 8,2"""

    //val inputs = s.split("\n").map(Line.parseLine).toVector
    val inputs = Source.fromFile("day5.txt").mkString.split("\n").map(Line.parseLine).toVector

    // Part 1

    val v = inputs.filter(l => l.isHorizontal || l.isVertical)

    var pointCounts: HashMap[(Int, Int), Int] = HashMap()

    v.foreach(l => l.generatePoints.foreach(p => pointCounts.update(p, pointCounts.getOrElse(p, 0) + 1) ))

    // Answer 1: 6005
    println(pointCounts.values.filter(x => x > 1).size)

    // Part 2

    pointCounts = HashMap()

    inputs.foreach(l => l.generatePoints.foreach(p => pointCounts.update(p, pointCounts.getOrElse(p, 0) + 1) ))

    // Answer 2: 23864
    println(pointCounts.values.filter(x => x > 1).size)
  }
}
