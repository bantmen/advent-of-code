import scala.io.Source
import scala.collection.mutable

import scala.util.control.Breaks._

object Day21 {

  def part1(x: Int, y: Int): Int = {
    var pos1 = x
    var pos2 = y

    var score1 = 0
    var score2 = 0

    var die = 1

    var dieRolls = 0

    var ans = -1

    // This code is no good. Part 2 is cleaner...
    breakable {
      while (true) {
        val roll1 = (1 to 3)
          .map(_ => {
            val temp = die
            die = if (die == 100) {
              1
            } else {
              die + 1
            }
            dieRolls += 1
            temp
          })
          .sum
        pos1 = if ((pos1 + roll1) % 10 == 0) {
          10
        } else {
          (pos1 + roll1) % 10
        }
        score1 += pos1
        if (score1 >= 1000) {
          ans = score2 * dieRolls
          break
        }

        val roll2 = (1 to 3)
          .map(_ => {
            val temp = die
            die = if (die == 100) {
              1
            } else {
              die + 1
            }
            dieRolls += 1
            temp
          })
          .sum
        pos2 = if ((pos2 + roll2) % 10 == 0) {
          10
        } else {
          (pos2 + roll2) % 10
        }
        score2 += pos2
        if (score2 >= 1000) {
          ans = score1 * dieRolls
          break
        }
      }
    }
    return ans
  }

  val rollSums: Seq[Int] = (1 to 3)
    .map(i => {
      (1 to 3).map(j => {
        (1 to 3).map(k => {
          i + j + k
        })
      })
    })
    .flatten
    .flatten

  def part2(
      score1: Int,
      pos1: Int,
      score2: Int,
      pos2: Int,
      player1Turn: Boolean,
      // Use memoization: game state -> (player 1 wins, player 2 wins)
      results: mutable.Map[(Int, Int, Int, Int, Boolean), (Long, Long)]
  ): (Long, Long) = {
    val t = (score1, pos1, score2, pos2, player1Turn)
    if (results.contains(t)) {
      results(t)
    } else if (score1 >= 21) {
      (1L, 0L)
    } else if (score2 >= 21) {
      (0L, 1L)
    } else {
      val ret = rollSums
        .map(roll => {
          if (player1Turn) {
            val newPos1 = if ((pos1 + roll) % 10 == 0) {
              10
            } else {
              (pos1 + roll) % 10
            }
            part2(score1 + newPos1, newPos1, score2, pos2, false, results)
          } else {
            val newPos2 = if ((pos2 + roll) % 10 == 0) {
              10
            } else {
              (pos2 + roll) % 10
            }
            part2(score1, pos1, score2 + newPos2, newPos2, true, results)
          }
        })
        .reduce((p1, p2) => (p1._1 + p2._1, p1._2 + p2._2))

      results(t) = ret
      ret
    }
  }

  def main(args: Array[String]): Unit = {
    val s = """Player 1 starting position: 9
Player 2 starting position: 4"""

    val Array(fst, snd) = s.split("\n").map(_.last.asDigit)

    // Answer 1: 998088
    println(part1(fst, snd))

    // Answer 2: 306621346123766
    println(part2(0, fst, 0, snd, true, mutable.HashMap()))
  }
}
