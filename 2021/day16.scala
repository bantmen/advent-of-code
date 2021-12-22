import scala.io.Source
import scala.collection.mutable

object Day16 {

  def toBin(hexS: String): String = {
    val s = BigInt(hexS, 16).toString(2)
    val numLeading = (Math.ceil(s.size / 4.0) * 4).toInt - s.size
    "0" * numLeading + s
  }

  def toInt(binS: String): Int = {
    Integer.parseInt(binS, 2)
  }

  def toLong(binS: String): Long = {
    BigInt(binS, 2).toLong
  }

  case class Literal(version: Int, packetType: Int, value: Long)

  case class Operator(
      version: Int,
      packetType: Int,
      subpackets: Seq[Either[Literal, Operator]]
  )

  case class ParseResult(
      packet: Either[Literal, Operator],
      endIndex: Int
  )

  def parse(s: String): ParseResult = {
    // version (0-2), packet type id (3-5)
    val version = toInt(s.slice(0, 3))
    val packetType = toInt(s.slice(3, 6))

    if (packetType == 4) {
      // Literal value
      // if packet type is 4, rest of the bits form groups (prefix 1) until the last group (prefix 0).
      // together these groups form a literal value.

      var onlySeenOne = true
      var numGroups = 0

      val literalS = s
        .slice(6, s.size)
        .sliding(size = 5, step = 5)
        .takeWhile(s => {
          if (!onlySeenOne) {
            false
          } else {
            onlySeenOne = s(0) == '1'
            numGroups += 1
            true
          }
        })
        .flatMap(group => group.slice(1, group.size))
        .mkString

      ParseResult(
        Left(Literal(version, packetType, toLong(literalS))),
        6 + numGroups * 5
      )
    } else {
      // Operator packet
      // otherwise, length type (6)
      val lengthType = s(6)

      if (lengthType == '0') {
        // bit length of the sub-packets (7 - 22)
        val length = toInt(s.slice(7, 22))

        val subpackets = mutable.ArrayBuffer[Either[Literal, Operator]]()

        var parsedBits = 0
        while (parsedBits < length) {
          val ParseResult(p, endIndex) = parse(
            s.slice(22 + parsedBits, s.size)
          )
          parsedBits += endIndex
          subpackets += p
        }

        assert(length == parsedBits)

        ParseResult(
          Right(Operator(version, packetType, Seq() ++ subpackets)),
          22 + length
        )
      } else {
        assert(lengthType == '1')

        // number of sub-packets (7 - 18)
        val num = toInt(s.slice(7, 18))

        var parsedBits = 0

        val subpackets = (1 to num).map(_ => {
          val ParseResult(p, endIndex) = parse(
            s.slice(18 + parsedBits, s.size)
          )
          parsedBits += endIndex
          p
        })

        ParseResult(
          Right(Operator(version, packetType, subpackets)),
          18 + parsedBits
        )
      }
    }
  }

  def versionSum(packet: Either[Literal, Operator]): Int = {
    packet match {
      case Left(p)  => p.version
      case Right(p) => p.version + p.subpackets.map(versionSum).sum
    }
  }

  def evaluate(packet: Either[Literal, Operator]): Long = {
    packet match {
      case Left(p) => p.value
      case Right(p) => {
        p.packetType match {
          case 0 => p.subpackets.map(evaluate).sum
          case 1 => p.subpackets.map(evaluate).product
          case 2 => p.subpackets.map(evaluate).min
          case 3 => p.subpackets.map(evaluate).max
          case 5 => {
            assert(p.subpackets.size == 2)
            if (evaluate(p.subpackets.head) > evaluate(p.subpackets.last)) {
              1
            } else {
              0
            }
          }
          case 6 => {
            assert(p.subpackets.size == 2)
            if (evaluate(p.subpackets.head) < evaluate(p.subpackets.last)) {
              1
            } else {
              0
            }
          }
          case 7 => {
            assert(p.subpackets.size == 2)
            if (evaluate(p.subpackets.head) == evaluate(p.subpackets.last)) {
              1
            } else {
              0
            }
          }
        }
      }
    }
  }

  def main(args: Array[String]): Unit = {
    val s =
      Source
        .fromFile("day16.txt")
        .mkString

    val ParseResult(p, _) = parse(toBin(s))

    // Answer 1: 873
    println(versionSum(p))

    // Answer 2: 402817863665
    println(evaluate(p))
  }
}
