import scala.io.Source
import scala.collection.mutable.Map


object Day6 {

  // state after day N -> state after day N + 1
  def step(state: Map[Long, Long]): Map[Long, Long] = {
    val newState = Map[Long, Long]().withDefaultValue(0)

    for ((k, v) <- state) {
      if (k == 0) {
        newState(6) += v
        newState(8) += v
      } else {
        newState(k - 1) += v
      }
    }

    newState
  }

  def run(initialState: Map[Long, Long], days: Int): Long = {
    var state = initialState
    for(i <- 0 until days){
        state = step(state)
    }
    state.values.sum
  }

  def main(args: Array[String]): Unit = {
    val inputs = Source.fromFile("day6.txt").mkString.split(",").map(_.toLong)

    // Operate on counts to save space
    var state = Map() ++ inputs.groupBy(identity).mapValues(_.size.toLong)

    // Answer 1: 345793
    println(run(state, 80))

    // Answer 2: 1572643095893
    println(run(state, 256))
  }
}
