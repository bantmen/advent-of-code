import scala.io.Source
import scala.collection.mutable.Set
import scala.collection.mutable

object Day12 {

  // Return num ways to traverse
  def traverse(
      node: String,
      graph: Map[String, Vector[String]],
      visited: mutable.Map[String, Int],
      usedSpecialSmallCave: Boolean
  ): Int = {
    if (node == "end") {
      1
    } else {
      graph(node)
        .map(node2 => {
          if (node2 == "start") {
            0
          } else if (
            visited(node2) == 0
            || (visited(node2) == 1 && !usedSpecialSmallCave)
            || node2.toUpperCase == node2
          ) {
            visited(node2) += 1

            var numVisit = 0
            if (visited(node2) == 2 && node2.toLowerCase == node2) {
              assert(!usedSpecialSmallCave)
              numVisit = traverse(node2, graph, visited, true)
            } else {
              numVisit = traverse(node2, graph, visited, usedSpecialSmallCave)
            }

            visited(node2) -= 1
            numVisit
          } else {
            0
          }
        })
        .sum
    }
  }

  def main(args: Array[String]): Unit = {
    val graph =
      Source
        .fromFile("day12.txt")
        .mkString
        .split("\n")
        .map(_.split("-"))
        .foldLeft(Map[String, Vector[String]]().withDefaultValue(Vector()))(
          (acc, l) =>
            // Edges are bidirectional
            acc + (l(0) -> (acc(l(0)) :+ l(1))) + (l(1) -> (acc(l(1)) :+ l(0)))
        )

    // Answer 1: 4775
    println(
      traverse(
        "start",
        graph,
        mutable.Map("start" -> 10).withDefaultValue(0),
        true
      )
    )

    // Answer 2: 152480
    println(
      traverse(
        "start",
        graph,
        mutable.Map("start" -> 10).withDefaultValue(0),
        false
      )
    )
  }
}
