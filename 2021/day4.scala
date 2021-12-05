import scala.io.Source


object Day4 {

  val NumRows = 5
  val NumCols = 5

  class WinnerFoundException(var ans: Int) extends Exception

  class Grid (val state: Array[Array[Int]], var playing: Boolean) {

    // Playing until a bingo

    def this(s: String) {
      this(Array.ofDim[Int](NumRows, NumCols), true)
      //val state2 = Array.ofDim[Int](NumRows, NumCols)
      val v = s.split("\n").toVector
      for (row <- 0 to NumRows - 1) {
        // There are sometimes multiple spaces between numbers
        // Need trim to handle left trailing space
        val rowV = v(row).trim.split(" +").toVector 
        for (col <- 0 to NumCols - 1) {
          state(row)(col) = rowV(col).toInt
        }
      }
    }

  }

  def main(args: Array[String]): Unit = {
    val s = """7,4,9,5,11,17,23,2,0,14,21,24,10,16,13,6,15,25,12,22,18,20,8,19,3,26,1

22 13 17 11  0
 8  2 23  4 24
21  9 14 16  7
 6 10  3 18  5
 1 12 20 15 19

 3 15  0  2 22
 9 18 13 17  5
19  8  7 25 23
20 11 10 24  4
14 21 16 12  6

14 21 17 24  4
10 16 15  9 19
18  8 23 26 20
22 11 13  6  5
 2  0 12  3  7"""

    //val inputs = s.split("\n\n").toVector
    val inputs = Source.fromFile("day4.txt").mkString.split("\n\n").toVector

    val numberDraws = inputs(0).split(",").map(_.toInt).toVector

    // Shared mutated state
    var grids = inputs.slice(1, inputs.size).map((s: String) => new Grid(s))
    var numWinners = 0

    val playGrid = (gridWrapper: Grid, draw: Int, findfirstWinner: Boolean) => {
      // How to early exit without nesting everything?
      if (gridWrapper.playing) {
        val grid = gridWrapper.state
        for (row <- 0 to grid.size - 1) {
          for (col <- 0 to grid(0).size - 1) {
            if (grid(row)(col) == draw) {
              grid(row)(col) = -1
              // Check if the row or column is now complete
              if (grid(row).forall(_ == -1) || grid.map(_(col)).forall(_ == -1)) {
                // Part 1 needs the first winner score. Part 2 the last winner.
                if (findfirstWinner || numWinners == grids.size - 1) {
                  // The answer is (sum of the remaining values in the grid) * draw
                  throw new WinnerFoundException(
                    grid.flatMap(_.toVector).filter(_ != -1).sum * draw)
                }
                numWinners += 1
                gridWrapper.playing = false
              }
            }
          }
        }
      }
    }

    try {
      numberDraws
        .foreach(
          draw => grids.foreach(
            grid => playGrid(grid, draw, true)))
    } catch {
      // Answer 1: 12796
      case ex: WinnerFoundException => println(ex.ans)
    }

    // Reset the state
    grids = inputs.slice(1, inputs.size).map((s: String) => new Grid(s))
    numWinners = 0

    try {
      numberDraws
        .foreach(
          draw => grids.foreach(
            grid => playGrid(grid, draw, false)))
    } catch {
      // Answer 2: 18063
      case ex: WinnerFoundException => println(ex.ans)
    }

  }
}
