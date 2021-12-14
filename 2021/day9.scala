import scala.io.Source
import scala.collection.mutable.Map

object Day9 {

  def inBounds(coord: (Int, Int), grid: Array[Array[Int]]): Boolean = {
    0 <= coord._1 && coord._1 < grid.size &&
    0 <= coord._2 && coord._2 < grid(0).size
  }

  def getNeighbourCoords(
      coord: (Int, Int),
      grid: Array[Array[Int]]
  ): Seq[(Int, Int)] = {
    Seq(
      (coord._1 - 1, coord._2),
      (coord._1, coord._2 - 1),
      (coord._1 + 1, coord._2),
      (coord._1, coord._2 + 1)
    ).filter(coord => inBounds(coord, grid))
  }

  def isLowPoint(coord: (Int, Int), grid: Array[Array[Int]]): Boolean = {
    getNeighbourCoords(coord, grid)
      .forall(newCoord =>
        grid(newCoord._1)(newCoord._2) > grid(coord._1)(coord._2)
      )
  }

  // Fill the coordToBasin
  def traverse(
      coord: (Int, Int),
      grid: Array[Array[Int]],
      coordToBasin: Map[(Int, Int), Int],
      basin: Int
  ): Unit = {
    if (grid(coord._1)(coord._2) != 9 && !coordToBasin.isDefinedAt(coord)) {
      coordToBasin(coord) = basin
      getNeighbourCoords(coord, grid)
        .foreach(newCoord => traverse(newCoord, grid, coordToBasin, basin))
    }
  }

  def main(args: Array[String]): Unit = {
    val grid =
      Source
        .fromFile("day9.txt")
        .mkString
        .split("\n")
        .map(_.toArray.map(_.asDigit))

    // Part 1

    var riskSum = 0
    for (row <- 0 to grid.size - 1) {
      for (col <- 0 to grid(0).size - 1) {
        if (isLowPoint((row, col), grid)) {
          riskSum += grid(row)(col) + 1
        }
      }
    }

    // Answer 1: 548
    println(riskSum)

    // Part 2

    val coordToBasin = Map[(Int, Int), Int]()

    var currentBasin = 0
    for (row <- 0 to grid.size - 1) {
      for (col <- 0 to grid(0).size - 1) {
        traverse((row, col), grid, coordToBasin, currentBasin)
        currentBasin += 1
      }
    }

    // Answer 2: 786048
    println(
      coordToBasin.values
        .groupBy(identity)
        .values
        .map(_.size)
        .toSeq
        .sorted
        .reverse
        .take(3)
        .reduce((x, y) => x * y)
    )

  }
}
