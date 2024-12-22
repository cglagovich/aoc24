import System.Environment (getArgs)
import Data.List

readInts :: [String] -> [Integer]
readInts = map read

parseInp :: String -> [[Integer]]
parseInp = map readInts . map words . lines

sortLists :: [[Integer]] -> [[Integer]]
sortLists = map sort . transpose

-- Returns a list of absolute differences
-- Transpose the list again and do the fold subtraction on the result
diffLists :: [[Integer]] -> [Integer]
diffLists lists = map (abs . foldl1 (-)) $ transpose lists


solve :: String -> Integer
solve = sum . diffLists . sortLists . parseInp

main :: IO ()
main = do
    args <- getArgs
    case args of
        [filename] -> readFile filename >>= putStrLn . show . solve
        _ -> putStrLn "Usage: program filename"