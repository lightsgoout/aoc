package main

import (
	"bufio"
	"fmt"
	"math"
	"os"
	"runtime"
	"strconv"
	"strings"
	"sync"
)

var cfg Config

type Range struct {
	Lo uint64
	Hi uint64
}

func main() {
	gold := uint64(math.MaxUint64)
	cfg = parse()

	silver := uint64(math.MaxUint64)
	for i := 0; i < len(cfg.Seeds); i++ {
		silver = min(silver, calc(cfg.Seeds[i]))
	}
	fmt.Printf("silver: %d\n", silver)

	output := make(chan uint64, 100000)
	input := make(chan Range)

	var wg sync.WaitGroup

	for i := 0; i < runtime.NumCPU(); i++ {
		wg.Add(1)
		go worker(input, output, &wg)
	}

	const batch = 100000
	for i := 0; i < len(cfg.Seeds); i += 2 {
		hi := cfg.Seeds[i] + cfg.Seeds[i+1]
		for lo := cfg.Seeds[i]; lo < hi; lo += batch {
			up := min(lo+batch, hi)
			input <- Range{Lo: lo, Hi: up}

		}
	}
	close(input)

	wg.Add(1)
	go func(_wg *sync.WaitGroup) {
		got := 0
		for res := range output {
			got++
			if got == runtime.NumCPU() {
				close(output)
			}
			gold = min(gold, res)
		}
		wg.Done()
	}(&wg)

	wg.Wait()
	fmt.Printf("gold: %d\n", gold)
}

func worker(input chan Range, result chan uint64, wg *sync.WaitGroup) {
	res := uint64(math.MaxUint64)
	for r := range input {
		for seed := r.Lo; seed < r.Hi; seed++ {
			res = min(res, calc(seed))
		}
	}
	result <- res
	wg.Done()
}

func calc(seed uint64) uint64 {
	for lvl := 1; lvl <= 7; lvl++ {
		gates := cfg.Gates[lvl]
		for _, g := range gates {
			if g.Src <= seed && seed < g.SrcHi {
				diff := seed - g.Src
				seed = g.Dst + diff
				break
			}
		}
	}
	return seed
}

type Config struct {
	Seeds []uint64
	Gates GateMap
}

type GateMap map[int][]GateInfo

type GateInfo struct {
	Dst   uint64
	Src   uint64
	SrcHi uint64
	Rng   uint64
}

func parse() Config {
	res := Config{}
	scanner := bufio.NewScanner(os.Stdin)
	gate := 0
	gates := make(GateMap)
	for scanner.Scan() {
		if line := scanner.Text(); len(line) != 0 {
			line = strings.TrimSpace(line)
			if line == "" {
				continue
			}
			if strings.HasPrefix(line, "seeds:") {
				seeds := make([]uint64, 0, 10)
				parts := strings.SplitN(line, ":", 2)
				for _, p := range strings.Split(parts[1], " ") {
					p = strings.TrimSpace(p)
					if p == "" {
						continue
					}
					seed, _ := strconv.Atoi(p)
					seeds = append(seeds, uint64(seed))
				}
				res.Seeds = seeds
				continue
			}

			if strings.Contains(line, "-to-") {
				gate += 1
				continue
			}

			parts := strings.Split(line, " ")
			dst, _ := strconv.Atoi(parts[0])
			src, _ := strconv.Atoi(parts[1])
			rng, _ := strconv.Atoi(parts[2])

			if len(gates[gate]) == 0 {
				gates[gate] = make([]GateInfo, 0, 10)
			}
			gates[gate] = append(gates[gate], GateInfo{
				Dst:   uint64(dst),
				Src:   uint64(src),
				SrcHi: uint64(src) + uint64(rng),
				Rng:   uint64(rng),
			})
		}
	}
	res.Gates = gates
	return res
}
