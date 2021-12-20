import scala.io.Source
import scala.collection.mutable

object Day15 {

  type Grid = Array[Array[Int]]

  def neighbours(
      coord: (Int, Int),
      rows: Int,
      cols: Int
  ): mutable.ArrayBuffer[(Int, Int)] = {
    val ret = mutable.ArrayBuffer[(Int, Int)]()
    val Tuple2(r, c) = coord
    if (r - 1 > -1) {
      ret += ((r - 1, c))
    }
    if (c - 1 > -1) {
      ret += ((r, c - 1))
    }
    if (r + 1 < rows) {
      ret += ((r + 1, c))
    }
    if (c + 1 < cols) {
      ret += ((r, c + 1))
    }
    ret
  }

  // The graph is a 2D array where neighbours are the adjacent tiles (no diagonals).
  def dijkstra(weights: Grid, from: (Int, Int), to: (Int, Int)): Int = {
    val rows = weights.size
    val cols = weights(0).size

    // We use a priority queue without a way to update the priorities (i.e. DECREASE-KEY)
    // See https://users.scala-lang.org/t/how-to-reprioritize-something-in-a-priority-queue/5604/9
    // on why this is tricky. tl;dr: Scala PriorityQueue does not support updates easily.
    // One alternative is to clone the priority queue after each update. That solution was taking
    // 18 minutes versus the following solution which takes <1s.
    // Instead of handling updates or deleting nodes and then enqueueing them again, we
    // enqueue for each update and ignore the state results:
    // https://stackoverflow.com/a/31123108/3712254
    // In practice, this is not only easier to implement (using standard library priority queues)
    // but also often faster.
    //
    // NOTE: This solution works regardless of the Set usage and I don't know why...
    val dist = Array.fill(rows, cols)(Int.MaxValue)
    dist(from._1)(from._2) = 0
    val pq = mutable.PriorityQueue[(Int, Int)]()(
      Ordering.by((c) => -dist(c._1)(c._2))
    )
    pq.enqueue(from)
    val S = mutable.Set[(Int, Int)]()

    while (!pq.isEmpty) {
      val u = pq.dequeue()
      if (!S.contains(u)) {
        S.add(u)
        for (v <- neighbours(u, rows, cols)) {
          val w = weights(v._1)(v._2)
          if (dist(v._1)(v._2) > dist(u._1)(u._2) + w) {
            dist(v._1)(v._2) = dist(u._1)(u._2) + w
            // there is no quick way to re-prioritize the queue.
            // instead, enqueue updates (duplicates) and ignore the stale nodes
            pq.enqueue(v)
          }
        }
      }
    }

    dist(to._1)(to._2)
  }

  def solve(grid: Grid): Int = {
    dijkstra(grid, (0, 0), (grid.size - 1, grid(0).size - 1))
  }

  def value(x: Int): Int = {
    if (x < 10) {
      x
    } else {
      x % 10 + 1
    }
  }

  def expandGrid(grid: Grid): Grid = {
    val numRepeat = 5
    val rows = grid.size
    val cols = grid(0).size

    val ret = Array.ofDim[Int](rows * numRepeat, cols * numRepeat)

    for (r <- 0 to rows - 1) {
      for (c <- 0 to cols - 1) {
        // repeat across columns
        for (i <- 0 to numRepeat - 1) {
          // repeat across rows
          for (j <- 0 to numRepeat - 1) {
            ret(r + i * rows)(c + j * cols) = value(grid(r)(c) + i + j)
          }
        }
      }
    }

    ret
  }

  def main(args: Array[String]): Unit = {
    val grid = Source
      .fromFile("day15.txt")
      .mkString
      .split("\n")
      .map(_.toArray.map(_.asDigit))

    // Answer 1: 720
    println(solve(grid))

    // Answer 2: 3025
    println(solve(expandGrid(grid)))
  }
}
