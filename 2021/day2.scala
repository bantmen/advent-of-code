import scala.io.Source


object Day2 {

  def main(args: Array[String]): Unit = {
    val l = Source.fromFile("day2.txt").getLines.toVector

    // coord: horizontal, depth
    val coords = l.foldLeft(0, 0)((coord: (Int, Int), line: String) => {
      val v = line.split(" ")
      val x = v(1).toInt
      v(0) match {
        case "forward" => (coord._1 + x, coord._2)
        case "down" => (coord._1, coord._2 + x)
        case "up" => (coord._1, coord._2 - x)
      }
    })

    // Answer 1: 1936494
    println(coords._1 * coords._2)

    // coord: horizontal, depth, aim
    val coords2 = l.foldLeft(0, 0, 0)((coord: (Int, Int, Int), line: String) => {
      val v = line.split(" ")
      val x = v(1).toInt
      v(0) match {
        case "forward" => (coord._1 + x, coord._2 + coord._3 * x, coord._3)
        case "down" => (coord._1, coord._2, coord._3 + x)
        case "up" => (coord._1, coord._2, coord._3 - x)
      }
    })

    // Answer 2: 1997106066
    println(coords2._1 * coords2._2)
  }
}
