import scala.io.Source
import scala.collection.mutable

import scala.util.control.Breaks._

object Day19 {

  val X = 1
  val Y = 2
  val Z = 3

  // Returns all 24 rotations
  def getRotations(): Seq[(Int, Int, Int)] = {
    val ret = mutable.Set[(Int, Int, Int)]()

    for (xy <- 0 to 3) {
      for (xz <- 0 to 3) {
        for (yz <- 0 to 3) {
          var Tuple3(x, y, z) = Tuple3(X, Y, Z)
          for (_ <- 0 to xy) {
            var temp = Tuple3(y, -x, z)
            x = temp._1
            y = temp._2
            z = temp._3
          }
          for (_ <- 0 to xz) {
            var temp = Tuple3(-z, y, x)
            x = temp._1
            y = temp._2
            z = temp._3
          }
          for (_ <- 0 to yz) {
            var temp = Tuple3(x, -z, y)
            x = temp._1
            y = temp._2
            z = temp._3
          }
          ret.add((x, y, z))
        }
      }
    }

    ret.toSeq
  }

  def helper(p: (Int, Int, Int), r: Int): Int = {
    if (r == X || r == -X) {
      p._1 * r.signum
    } else if (r == Y || r == -Y) {
      p._2 * r.signum
    } else {
      p._3 * r.signum
    }
  }

  def transform(
      pts: Set[(Int, Int, Int)],
      rot: (Int, Int, Int)
  ): Set[(Int, Int, Int)] = {
    pts
      .map(p => {
        (helper(p, rot._1), helper(p, rot._2), helper(p, rot._3))
      })
      .toSet
  }

  def add(
      pts: Set[(Int, Int, Int)],
      s: (Int, Int, Int)
  ): Set[(Int, Int, Int)] = {
    pts
      .map(p => {
        (p._1 + s._1, p._2 + s._2, p._3 + s._3)
      })
      .toSet
  }

  // Use Scanner 0 as pts1.
  // Returns the scanner location of pts2 if there is alignment
  def align(
      pts1: Set[(Int, Int, Int)],
      pts2: Set[(Int, Int, Int)]
  ): Option[(Int, Int, Int)] = {
    val m = mutable.Map[(Int, Int, Int), Int]().withDefaultValue(0)
    for (p1 <- pts1) {
      for (p2 <- pts2) {
        // When there is alignment, s1 + p1 = s2 + p2
        // Since Scanner 0 is the point of reference, s1 is assumed to be (0, 0)
        // Thus s2 = p1 - p2
        val diff = (p1._1 - p2._1, p1._2 - p2._2, p1._3 - p2._3)
        m(diff) += 1
      }
    }
    val Tuple2(s2, freq) = m.maxBy(_._2)
    if (freq >= 12) {
      Some(s2)
    } else {
      None
    }
  }

  def manhattan(p1: (Int, Int, Int), p2: (Int, Int, Int)): Int = {
    (p1._1 - p2._1).abs + (p1._2 - p2._2).abs + (p1._3 - p2._3).abs
  }

  def main(args: Array[String]): Unit = {
    val s =
      Source
        .fromFile("day19.txt")
        .mkString

    // List of each scanner's points
    val x = s
      .split("\n\n")
      .map(scannerSegment => {
        // List of 3d points
        scannerSegment
          .split("\n")
          .tail
          .map(line => {
            val temp = line.split(",").map(_.toInt)
            (temp(0), temp(1), temp(2))
          })
          .toSet
      })
      .toVector

    var pts1: Set[(Int, Int, Int)] = x(0)
    var rest: Vector[Set[(Int, Int, Int)]] = x.tail

    val rotations = getRotations()

    var scanners = Vector[(Int, Int, Int)]()

    while (!rest.isEmpty) {
      breakable {
        for (pair <- rest.zipWithIndex) {
          val Tuple2(pts2, idx) = pair

          for (rot <- rotations) {
            val newPts2 = transform(pts2, rot)

            align(pts1, newPts2) match {
              case Some(x) => {
                val relPts2 = add(newPts2, x)
                scanners = scanners ++ Vector(x)
                pts1 = pts1 ++ relPts2
                rest = rest.patch(from = idx, patch = Nil, replaced = 1)
                break
              }
              case None => {}
            }
          }
        }
      }
    }

    // Answer 1: 438
    println(pts1.size)

    // Answer 2: 11985
    println(
      scanners
        .map(p => {
          scanners
            .map(p2 => {
              manhattan(p, p2)
            })
            .max
        })
        .max
    )

  }
}
