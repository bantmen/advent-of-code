import scala.io.Source

object Day7 {

  def main(args: Array[String]): Unit = {
    val inputs = Source.fromFile("day7.txt").mkString.split(",").map(_.toInt)

    // Answer 1: 325528
    println(
        (inputs.min to inputs.max)
        .map(x => inputs.map(i => (i - x).abs).sum)
        .min)

    // Answer 2: 85015836
    println(
        (inputs.min to inputs.max)
        .map(x => inputs.map(i => ((i - x).abs) * ((i - x).abs + 1) / 2).sum)
        .min)
  }

}