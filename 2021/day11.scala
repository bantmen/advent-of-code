import scala.io.Source
import scala.collection.mutable.Set

object Day11 {

  def gridCoords(grid: Array[Array[Int]]): Seq[(Int, Int)] = {
    for {
      row <- 0 to grid.size - 1
      col <- 0 to grid(0).size - 1
    } yield (row, col)
  }

  def inBounds(coord: (Int, Int), grid: Array[Array[Int]]): Boolean = {
    0 <= coord._1 && coord._1 < grid.size &&
    0 <= coord._2 && coord._2 < grid(0).size
  }

  def neighbourCoords(
      coord: (Int, Int),
      grid: Array[Array[Int]]
  ): Seq[(Int, Int)] = {
    val seq = for {
      d1 <- (-1 to 1)
      d2 <- (-1 to 1)
      if (d1 != 0 || d2 != 0)
    } yield (
      coord._1 + d1,
      coord._2 + d2
    )
    seq.filter(coord => inBounds(coord, grid))
  }

  // Return num flashed in this traversal
  def traverse(
      coord: (Int, Int),
      grid: Array[Array[Int]],
      usedAllEnergy: Set[(Int, Int)]
  ): Int = {
    if (usedAllEnergy.contains(coord)) {
      0
    } else if (grid(coord._1)(coord._2) == 9) {
      usedAllEnergy.add(coord)
      grid(coord._1)(coord._2) = 0
      1 + neighbourCoords(coord, grid)
        .map(newCoord => traverse(newCoord, grid, usedAllEnergy))
        .sum
    } else {
      grid(coord._1)(coord._2) += 1
      0
    }
  }

  // Num flashed in one turn
  def play(grid: Array[Array[Int]]): Int = {
    val usedAllEnergy = Set[(Int, Int)]()
    gridCoords(grid).map(coord => traverse(coord, grid, usedAllEnergy)).sum
  }

  def allZero(grid: Array[Array[Int]]): Boolean = {
    gridCoords(grid).forall(coord => grid(coord._1)(coord._2) == 0)
  }

  def main(args: Array[String]): Unit = {
    val grid =
      Source
        .fromFile("day11.txt")
        .mkString
        .split("\n")
        .map(_.toArray.map(_.asDigit))

    // Answer 1: 1620
    println(
      (1 to 100).map(i => play(grid)).sum
    )

    val grid2 =
      Source
        .fromFile("day11.txt")
        .mkString
        .split("\n")
        .map(_.toArray.map(_.asDigit))

    // Answer 2: 371
    println(
      (1 to 1000)
        .takeWhile(_ => !allZero(grid2) && play(grid2) >= 0)
        .last
    )
  }
}
