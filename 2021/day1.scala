import scala.io.Source


object Day1 {

  def numGreaterWindowTwo(v: Vector[Int]): Int = {
    v.sliding(size=2, step=1)
     .foldLeft(0)((acc: Int, v: Vector[Int]) =>  
       if (v(1) > v(0)) {
         acc + 1
       } else {
         acc
       }
    )
  }

  def main(args: Array[String]): Unit = {
    val l = Source.fromFile("day1.txt").getLines.toVector.map(_.toInt)
    // Answer 1: 1482
    println(numGreaterWindowTwo(l))

    val l2 = l.sliding(size=3, step=1).toVector.map(_.sum)
    // Answer 2: 1518
    println(numGreaterWindowTwo(l2))
  }
}
