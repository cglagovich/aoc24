import System.Environment (getArgs)
import Data.List

-- trying to implement solve like Claude
solvep1 :: String -> Integer
solvep1 inp = sum $ zipWith (\a b -> abs(a - b)) sortedLeft sortedRight
    where
        (leftnums, rightnums) = unzip [(read l, read r) | line <- lines inp, let [l, r] = words line]
        sortedLeft = sort leftnums
        sortedRight = sort rightnums

solvep2 :: String -> Integer
solvep2 inp = sum $ zipWith (*) lhs rhs_count
    where
        (lhs, rhs) = unzip [(read l, read r) | line <- lines inp, let [l, r] = words line]
        rhs_count = [foldl (\acc x -> if x == needle then (acc+1) else acc) 0 rhs | needle <- lhs]


main :: IO ()
main = do
    args <- getArgs
    case args of
        [filename] -> do
            inp <- readFile filename
            putStrLn $ show $ solvep1 inp
            putStrLn $ show $ solvep2 inp
        _ -> putStrLn "Usage: program filename"