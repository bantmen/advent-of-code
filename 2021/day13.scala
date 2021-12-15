import scala.io.Source
import scala.collection.mutable

object Day13 {

  def main(args: Array[String]): Unit = {
    val s = """6,10
0,14
9,10
0,3
10,4
4,11
6,0
6,12
4,1
0,13
10,12
3,4
3,0
8,4
1,10
2,14
8,10
9,0

fold along y=7
fold along x=5"""

    val Array(first, second) =
      // s
      Source
        .fromFile("day13.txt")
        .mkString
        .split("\n\n")
        .map(_.split("\n"))

    // (x, y) or (columns, rows)
    var coords = first
      .map(_.split(",").map(_.toInt))
      .map(l => (l(0), l(1)))
      .toSet

    val instructions =
      second.map(_.split(" ")(2).split("=")).map(l => (l(0), l(1).toInt))

    for (instr <- instructions) {
      val k = instr._2
      instr._1 match {
        case "y" => {
          val pt1 = coords.filter(c => c._2 <= k)
          val pt2 = coords
            .filter(c => c._2 > k)
            .map(c => (c._1, k * 2 - c._2))
          coords = pt1 ++ pt2
        }
        case "x" => {
          val pt1 = coords.filter(c => c._1 <= k)
          val pt2 = coords
            .filter(c => c._1 > k)
            .map(c => (k * 2 - c._1, c._2))
          coords = pt1 ++ pt2
        }
      }
      // Answer: 618
      // First print is the answer
      println(coords.size)
    }

    val maxY = coords.map(_._2).max
    val maxX = coords.map(_._1).max

    val dense = Array.ofDim[String](maxY + 1, maxX + 1)

    for (y <- (0 to maxY); x <- (0 to maxX)) {
      if (coords.contains((x, y))) {
        dense(y)(x) = "⬛"
      } else {
        dense(y)(x) = " "
      }
    }

    // Answer 2
    dense.foreach(row => println(row.toVector.mkString))

  }
}
