import scala.io.Source
import scala.math.round


object Day3 {


  def main(args: Array[String]): Unit = {

    val s = """00100
11110
10110
10111
10101
01111
00111
11100
10000
11001
00010
01010"""

    //val l = s.split("\n").toVector.map(_.toVector.map(_.asDigit))

    val l = Source.fromFile("day3.txt").getLines.toVector.map(_.toVector.map(_.asDigit))

    val numEntries = l.size

    val digitSum = l.foldLeft(Vector.fill(12)(0))((acc: Vector[Int], v: Vector[Int]) => {
      acc.zip(v).map { case (x, y) => x + y }
    })

    // Part 1

    val gamma = digitSum.map((e: Int) => { (e.toFloat / numEntries).round })
    val epsilon = gamma.map((e: Int) => { (1 - e).abs } )

    val toBinary = (v: Vector[Int]) => {Integer.parseInt(v.mkString, 2)}

    // Answer 1: 4001724
    println(toBinary(gamma) * toBinary(epsilon))

    // Part 2

    // For each index 
    // - find the dominant bit (0 vs 1)
    // - filter by the dominant bit
    // - stop if only one entry remaning

    var l2 = l

    val filterMostCommon = (i: Int) => {
      val mostCommon = l2.map(_(i)).sum >= l2.size / 2.0 match {
        case true => 1
        case false => 0
      }
      if (l2.size > 1) {
        l2 = l2.filter(_(i) == mostCommon)
      }
    }

    (0 to l2(0).size - 1).takeWhile(_ => l2.size > 1).foreach(i => filterMostCommon(i))

    assert(l2.size == 1)
    val oxygen = l2(0)

    l2 = l

    val filterLeastCommon = (i: Int) => {
      val leastCommon = l2.map(_(i)).sum < l2.size / 2.0 match {
        case true => 1
        case false => 0
      }
      if (l2.size > 1) {
        l2 = l2.filter(_(i) == leastCommon)
      }
      println(i, leastCommon)
    }

    (0 to l2(0).size - 1).takeWhile(_ => l2.size > 1).foreach(i => filterLeastCommon(i))

    assert(l2.size == 1)
    val co2 = l2(0)

    // Answer 2: 587895
    println(toBinary(oxygen) * toBinary(co2))

  }


}

