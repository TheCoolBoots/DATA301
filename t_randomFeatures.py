import unittest
import randomFeatures

class t_randomFeatures(unittest.TestCase):

    def test_getRandom(self):
        randomNum = randomFeatures.getRandomSmallInt()
        self.assertTrue(0 <= randomNum and randomNum <= 9)

    def test_failure(self):
        self.assertTrue(False)


if __name__ == '__main__':
    unittest.main()

"""
C#
using Microsoft.VisualStudio.TestTools.UnitTesting;

namespace BankTests
{
    [TestClass]
    public class BankAccountTests
    {
        [TestMethod]
        public void TestMethod1()
        {
        }
    }
}
"""