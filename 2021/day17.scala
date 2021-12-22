import scala.io.Source
import scala.collection.mutable

object Day17 {

  // Return max height if projectile gets within the area
  def simulate(
      x1: Int,
      x2: Int,
      y1: Int,
      y2: Int,
      v_x: Int,
      v_y: Int
  ): Option[Int] = {
    var x = 0
    var y = 0
    var vx = v_x
    var vy = v_y

    var maxY = Int.MinValue

    var gotWithin = false

    while (x <= x2 && y >= y1) {
      x += vx
      y += vy

      maxY = Math.max(y, maxY)

      if (x >= x1 && x2 >= x && y >= y1 && y2 >= y) {
        gotWithin = true
      }

      vx = Math.max(vx - 1, 0)
      vy -= 1
    }

    if (gotWithin) {
      Some(maxY)
    } else {
      None
    }
  }

  def main(args: Array[String]): Unit = {
    val x1 = 192
    val x2 = 251
    val y1 = -89
    val y2 = -59

    var vx = 6
    var vy = 9

    var maxY = Int.MinValue
    var numWithin = 0

    for (vy <- 100 to y1 by -1) {
      for (vx <- 0 to x2) {
        simulate(x1, x2, y1, y2, vx, vy) match {
          case Some(y) => {
            maxY = Math.max(maxY, y)
            numWithin += 1
          }
          case None => -1
        }
      }
    }

    // Answer 1: 3916
    println(maxY)

    // Answer 2:
    println(numWithin)
  }
}
