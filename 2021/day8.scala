import scala.io.Source
import scala.collection.mutable.Map

object Day8 {

  def decode(tenDigits: Array[String], fourDigitOutput: Array[String]): Int = {
    val counts = Map[Char, Int]().withDefaultValue(0)
    tenDigits.foreach(_.map(c => counts(c) += 1))

    // Deduct e, b, and f from frequencies
    val mapping = Map[Char, Char]()
    mapping('e') = counts.find(_._2 == 4) match {
      case Some(x) => x._1
      case _       => 'z' // Should not happen
    }
    mapping('b') = counts.find(_._2 == 6) match {
      case Some(x) => x._1
      case _       => 'z' // Should not happen
    }
    mapping('f') = counts.find(_._2 == 9) match {
      case Some(x) => x._1
      case _       => 'z' // Should not happen
    }

    // Deduct the rest of the characters
    tenDigits
      .sortBy(_.size)
      .foreach(s =>
        s.size match {
          case 2 => {
            // 1 contains c, f. determine c
            mapping('c') = if (s(0) != mapping('f')) {
              s(0)
            } else {
              s(1)
            }
          }
          case 3 => {
            // 7 contains a, c, f. determine a
            s.foreach(c => {
              if (c != mapping('c') && c != mapping('f')) {
                mapping('a') = c
              }
            })
          }
          case 4 => {
            // 4 contains b, c, d, f. determine d
            s.foreach(c => {
              if (c != mapping('b') && c != mapping('c') && c != mapping('f')) {
                mapping('d') = c
              }
            })
          }
          case 7 => {
            // 8 contains all characters. determine g
            s.foreach(c => {
              if (!mapping.values.toVector.contains(c)) {
                mapping('g') = c
              }
            })
          }
          case _ => 1
        }
      )

    val segmentToDigit = Map(
      "abcefg" -> 0,
      "cf" -> 1,
      "acdeg" -> 2,
      "acdfg" -> 3,
      "bcdf" -> 4,
      "abdfg" -> 5,
      "abdefg" -> 6,
      "acf" -> 7,
      "abcdefg" -> 8,
      "abcdfg" -> 9
    )

    val inverseMapping = Map() ++ mapping.map(_.swap)

    fourDigitOutput
      .map(_.map(c => inverseMapping(c)))
      .map(s => segmentToDigit(s.sorted))
      .mkString
      .toInt
  }

  def main(args: Array[String]): Unit = {
    // entries: ([ten unique digits], [four output digits])
    val inputs = Source
      .fromFile("day8.txt")
      .mkString
      .split("\n")
      .map(_.split(" \\| ").map(_.split(" ")))

    // 1 (2), 4 (4), 7 (3), 8 (7)
    val easyDigitLengths = Vector(2, 4, 3, 7)

    // Answer 1: 554
    println(
      inputs
        .map(_(1))
        .map(_.filter(s => easyDigitLengths.contains(s.size)).size)
        .sum
    )

    // Answer 2: 990964
    println(inputs.map(l => decode(l(0), l(1))).sum)
  }
}
