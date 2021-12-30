import scala.io.Source
import scala.collection.mutable

object Day20 {

  val Light = '#'
  val Dark = '.'

  def outside(p: (Int, Int), b1: (Int, Int), b2: (Int, Int)): Boolean = {
    p._1 < b1._1 || p._2 < b1._2 || p._1 > b2._1 || p._2 > b2._2
  }

  def neighbour(
      grid: Set[(Int, Int)],
      p: (Int, Int),
      b1: (Int, Int),
      b2: (Int, Int),
      turn: Int
  ): Seq[Int] = {
    // [p0 - 1, p0 + 1] x [p1 - 1, p1 + 1]
    (p._1 - 1 to p._1 + 1)
      .flatMap(i => {
        (p._2 - 1 to p._2 + 1).map(j => {
          // Assume that lookup.first is Light and lookup.last is Dark
          if (
            grid.contains((i, j))
            || (turn % 2 == 0 && outside((i, j), b1, b2))
          ) {
            1
          } else {
            0
          }
        })
      })
  }

  def step(
      grid: Set[(Int, Int)],
      lookup: Vector[Char],
      turn: Int
  ): Set[(Int, Int)] = {
    val xMin = grid.minBy(_._1)._1
    val xMax = grid.maxBy(_._1)._1
    val yMin = grid.minBy(_._2)._2
    val yMax = grid.maxBy(_._2)._2

    (xMin - 2 to xMax + 2)
      .flatMap(i => {
        (yMin - 2 to yMax + 2).map(j => {
          val bin = neighbour(grid, (i, j), (xMin, yMin), (xMax, yMax), turn)
          val x = Integer.parseInt(bin.mkString, 2)
          if (lookup(x) == Light) {
            Some((i, j))
          } else {
            None
          }
        })
      })
      .flatten // unwrap Options
      .toSet
  }

  def main(args: Array[String]): Unit = {
    val s =
      Source
        .fromFile("day20.txt")
        .mkString

    val Array(fst, tmp) = s.split("\n\n")

    val snd = tmp.split("\n").map(_.toVector)

    val lookup = fst.toVector

    val tempGrid = mutable.Set[(Int, Int)]()

    for (i <- 0 to snd.size - 1) {
      for (j <- 0 to snd(0).size - 1) {
        if (snd(i)(j) == Light) {
          tempGrid.add((i, j))
        }
      }
    }

    var grid = tempGrid.toSet

    for (turn <- (1 to 2)) {
      grid = step(grid, lookup, turn)
    }

    // Answer 1: 5179
    println(grid.size)

    grid = tempGrid.toSet

    for (turn <- (1 to 50)) {
      grid = step(grid, lookup, turn)
    }

    // Answer 2: 16112
    println(grid.size)
  }
}
