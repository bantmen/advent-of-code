import scala.io.Source
import scala.collection.mutable

object Day14 {

  // For part 2 my initial attempt to speed up the solution only used the window,
  // and when that didn't work, we also end up with a mutable char count map. it
  // was too difficult to refactor the char counts into an immutable map
  // so it's left as is.
  //
  // window: use the counts to quickly apply the rules
  // char: counts max - min give the question's answer
  case class Counts(window: Map[String, Long], char: mutable.Map[Char, Long])

  def step(
      counts: Counts,
      rules: Map[String, String]
  ): Counts = {
    val newWindow =
      counts.window.foldLeft(Map[String, Long]().withDefaultValue(0L))(
        (
            acc: Map[String, Long],
            p: (String, Long)
        ) => {
          val Tuple2(s, x) = p
          val c = rules(s)
          counts.char(c(0)) = counts.char(c(0)) + x
          acc +
            ((s(0) + c) -> (acc(s(0) + c) + x)) +
            ((c + s(1)) -> (acc(c + s(1)) + x))
        }
      )
    Counts(newWindow, counts.char)
  }

  def solve(rules: Map[String, String], counts: Counts, N: Int): Long = {
    val newCounts =
      (1 to N).foldLeft(counts)((acc, _) => step(acc, rules))
    newCounts.char.values.max - newCounts.char.values.min
  }

  def main(args: Array[String]): Unit = {

    val Array(polymer, rulesStr) = Source
      .fromFile("day14.txt")
      .mkString
      .split("\n\n")

    val rules =
      rulesStr.split("\n").map(_.split(" -> ")).map(l => (l(0), l(1))).toMap

    val windowCounts = polymer
      .sliding(size = 2, step = 1)
      .toSeq
      .groupBy(identity)
      .mapValues(_.size.toLong)

    val charCounts = mutable.Map().withDefaultValue(0L) ++ polymer
      .groupBy(identity)
      .mapValues(_.size.toLong)

    // Answer 1: 2223
    println(solve(rules, Counts(windowCounts, charCounts.clone()), 10))

    // Answer 2: 2566282754493
    println(solve(rules, Counts(windowCounts, charCounts.clone()), 40))

  }
}
