# zilliqa-difficulty

Simulations of the Zilliqa difficulty adjustment algorithm.

## Writeup

### Introduction

Difficulty in Zilliqa is represented as an integer representing the number of zero bits prefixing a
'boundary' value. Solutions are determined to be valid or not by checking that the value of the
Ethash candidate is lower than this boundary.

Therefore, the solution space effectively decreases on a logarithmic scale as the difficulty
increases. Every time the difficulty increases by 1, the expected number of hashes required
increases by a factor of two.

Each solution allows a miner to 'purchase' a ticket into the network. However, there is a maximum
number of tickets allowed into the network. The difficulty is adjusted based on the deviation from
this maximum number of tickets.

At the time of writing, the target is set at 1810 tickets and the deviation is set at 100. For
every 100 more or fewer tickets submitted compared to this target, the difficulty will be increased
or decreased by 1.

### Problem

The use of a logarithmic scale would prove problematic in practice.

As can be observed in the last few epochs, the shard difficulty has had problems maintaining a
stable rate. This is particularly apparent as the network goes into higher difficulty values.

```
Epoch 137: (Diff 34 (17 Gh | 286 Mh/s), 40 (1100 Gh | 18 Gh/s).
Epoch 138: (Diff 32 (4 Gh | 72 Mh/s), 40 (1100 Gh | 18 Gh/s).
Epoch 139: (Diff 34 (17 Gh | 286 Mh/s), 39 (550 Gh | 9 Gh/s).
Epoch 140: (Diff 32 (4 Gh | 72 Mh/s), 40 (1100 Gh | 18 Gh/s).
Epoch 141: (Diff 34 (17 Gh | 286 Mh/s), 40 (1100 Gh | 18 Gh/s).
Epoch 142: (Diff 32 (4 Gh | 72 Mh/s), 39 (550 Gh | 9 Gh/s).
Epoch 143: (Diff 34 (17 Gh | 286 Mh/s), 40 (1100 Gh | 18 Gh/s).
Epoch 144: (Diff 32 (4 Gh | 72 Mh/s), 40 (1100 Gh | 18 Gh/s).
Epoch 145: (Diff 34 (17 Gh | 286 Mh/s), 40 (1100 Gh | 18 Gh/s).
Epoch 146: (Diff 32 (4 Gh | 72 Mh/s), 40 (1100 Gh | 18 Gh/s).
Epoch 147: (Diff 34 (17 Gh | 286 Mh/s), 40 (1100 Gh | 18 Gh/s).
Epoch 148: (Diff 32 (4 Gh | 72 Mh/s), 40 (1100 Gh | 18 Gh/s).
Epoch 149: (Diff 34 (17 Gh | 286 Mh/s), 40 (1100 Gh | 18 Gh/s).
Epoch 150: (Diff 32 (4 Gh | 72 Mh/s), 40 (1100 Gh | 18 Gh/s).
Epoch 151: (Diff 34 (17 Gh | 286 Mh/s), 40 (1100 Gh | 18 Gh/s).
Epoch 152: (Diff 32 (4 Gh | 72 Mh/s), 40 (1100 Gh | 18 Gh/s).
Epoch 153: (Diff 34 (17 Gh | 286 Mh/s), 40 (1100 Gh | 18 Gh/s).
Epoch 154: (Diff 32 (4 Gh | 72 Mh/s), 40 (1100 Gh | 18 Gh/s).
Epoch 155: (Diff 34 (17 Gh | 286 Mh/s), 40 (1100 Gh | 18 Gh/s).
Epoch 156: (Diff 32 (4 Gh | 72 Mh/s), 40 (1100 Gh | 18 Gh/s).
Epoch 157: (Diff 34 (17 Gh | 286 Mh/s), 40 (1100 Gh | 18 Gh/s).
Epoch 158: (Diff 33 (9 Gh | 143 Mh/s), 40 (1100 Gh | 18 Gh/s).
Epoch 159: (Diff 35 (34 Gh | 573 Mh/s), 40 (1100 Gh | 18 Gh/s).
Epoch 160: (Diff 33 (9 Gh | 143 Mh/s), 40 (1100 Gh | 18 Gh/s).
Epoch 161: (Diff 35 (34 Gh | 573 Mh/s), 40 (1100 Gh | 18 Gh/s).
Epoch 162: (Diff 33 (9 Gh | 143 Mh/s), 40 (1100 Gh | 18 Gh/s).
Epoch 163: (Diff 35 (34 Gh | 573 Mh/s), 40 (1100 Gh | 18 Gh/s).
Epoch 164: (Diff 33 (9 Gh | 143 Mh/s), 40 (1100 Gh | 18 Gh/s).
Epoch 165: (Diff 35 (34 Gh | 573 Mh/s), 40 (1100 Gh | 18 Gh/s).
Epoch 166: (Diff 33 (9 Gh | 143 Mh/s), 40 (1100 Gh | 18 Gh/s).
Epoch 167: (Diff 35 (34 Gh | 573 Mh/s), 39 (550 Gh | 9 Gh/s).
Epoch 168: (Diff 33 (9 Gh | 143 Mh/s), 41 (2199 Gh | 37 Gh/s).
Epoch 169: (Diff 35 (34 Gh | 573 Mh/s), 41 (2199 Gh | 37 Gh/s).
Epoch 170: (Diff 33 (9 Gh | 143 Mh/s), 40 (1100 Gh | 18 Gh/s).
Epoch 171: (Diff 35 (34 Gh | 573 Mh/s), 40 (1100 Gh | 18 Gh/s).
```

The difficulty values tend to see-saw between two values instead of staying stable. This is
primarily caused by the actual network hashrate sitting between the two difficulties. Due to the
logarithmic scale, and the fact that the number of nodes is not easily variable, the difficulty
fails to find any stability.

This causes issues with miners as the jump in required hashrate can be extremely large, especially
at the higher values. For the difficulty to maintain stability, the network hashrate has to be
extremely close to one of the following values:

```
Global hashrate required to maintain 1810 nodes:
Diff 00 =       10 H/s
Diff 01 =       20 H/s
Diff 02 =       40 H/s
Diff 03 =       81 H/s
Diff 04 =      162 H/s
Diff 05 =      325 H/s
Diff 06 =      650 H/s
Diff 07 =       1 Kh/s
Diff 08 =       3 Kh/s
Diff 09 =       5 Kh/s
Diff 10 =      10 Kh/s
Diff 11 =      21 Kh/s
Diff 12 =      42 Kh/s
Diff 13 =      83 Kh/s
Diff 14 =     167 Kh/s
Diff 15 =     333 Kh/s
Diff 16 =     666 Kh/s
Diff 17 =       1 Mh/s
Diff 18 =       3 Mh/s
Diff 19 =       5 Mh/s
Diff 20 =      11 Mh/s
Diff 21 =      21 Mh/s
Diff 22 =      43 Mh/s
Diff 23 =      85 Mh/s
Diff 24 =     171 Mh/s
Diff 25 =     341 Mh/s
Diff 26 =     682 Mh/s
Diff 27 =       1 Gh/s
Diff 28 =       3 Gh/s
Diff 29 =       5 Gh/s
Diff 30 =      11 Gh/s
Diff 31 =      22 Gh/s
Diff 32 =      44 Gh/s
Diff 33 =      87 Gh/s
Diff 34 =     175 Gh/s
Diff 35 =     349 Gh/s
Diff 36 =     699 Gh/s
Diff 37 =       1 Th/s
Diff 38 =       3 Th/s
Diff 39 =       6 Th/s
Diff 40 =      11 Th/s
Diff 41 =      22 Th/s
Diff 42 =      45 Th/s
Diff 43 =      89 Th/s
Diff 44 =     179 Th/s
Diff 45 =     358 Th/s
Diff 46 =     715 Th/s
Diff 47 =    1431 Th/s
Diff 48 =    2862 Th/s
Diff 49 =    5723 Th/s
--------------------------------------------------------
```

If at any time the network hashrate lies between any of these values, the difficulty will see-saw.

A model of a hypothetical network with the difficulty starting at 32, the constant network
hashrate of 58 Gh/s, and a maximum cap of 2100 nodes demonstrates that this see-sawing does not stop
even after 50 iterations.

```
Simulating for 50 epochs:
Starting Difficulty: 32
Global Hashrate: 58 Gh/s
n=01  solutions=2010  difficulty=34  adjustment=2
n=02  solutions=1402  difficulty=29  adjustment=-4
n=03  solutions=2100  difficulty=31  adjustment=2
n=04  solutions=2100  difficulty=33  adjustment=2
n=05  solutions=1605  difficulty=31  adjustment=-2
n=06  solutions=2100  difficulty=33  adjustment=2
n=07  solutions=1605  difficulty=31  adjustment=-2
n=08  solutions=2100  difficulty=33  adjustment=2
n=09  solutions=1605  difficulty=31  adjustment=-2
n=10  solutions=2100  difficulty=33  adjustment=2
n=11  solutions=1605  difficulty=31  adjustment=-2
n=12  solutions=2100  difficulty=33  adjustment=2
n=13  solutions=1605  difficulty=31  adjustment=-2
n=14  solutions=2100  difficulty=33  adjustment=2
n=15  solutions=1605  difficulty=31  adjustment=-2
n=16  solutions=2100  difficulty=33  adjustment=2
n=17  solutions=1605  difficulty=31  adjustment=-2
n=18  solutions=2100  difficulty=33  adjustment=2
n=19  solutions=1605  difficulty=31  adjustment=-2
n=20  solutions=2100  difficulty=33  adjustment=2
n=21  solutions=1605  difficulty=31  adjustment=-2
n=22  solutions=2100  difficulty=33  adjustment=2
n=23  solutions=1605  difficulty=31  adjustment=-2
n=24  solutions=2100  difficulty=33  adjustment=2
n=25  solutions=1605  difficulty=31  adjustment=-2
n=26  solutions=2100  difficulty=33  adjustment=2
n=27  solutions=1605  difficulty=31  adjustment=-2
n=28  solutions=2100  difficulty=33  adjustment=2
n=29  solutions=1605  difficulty=31  adjustment=-2
n=30  solutions=2100  difficulty=33  adjustment=2
n=31  solutions=1605  difficulty=31  adjustment=-2
n=32  solutions=2100  difficulty=33  adjustment=2
n=33  solutions=1605  difficulty=31  adjustment=-2
n=34  solutions=2100  difficulty=33  adjustment=2
n=35  solutions=1605  difficulty=31  adjustment=-2
n=36  solutions=2100  difficulty=33  adjustment=2
n=37  solutions=1605  difficulty=31  adjustment=-2
n=38  solutions=2100  difficulty=33  adjustment=2
n=39  solutions=1605  difficulty=31  adjustment=-2
n=40  solutions=2100  difficulty=33  adjustment=2
n=41  solutions=1605  difficulty=31  adjustment=-2
n=42  solutions=2100  difficulty=33  adjustment=2
n=43  solutions=1605  difficulty=30  adjustment=-2
n=44  solutions=2100  difficulty=32  adjustment=2
n=45  solutions=2010  difficulty=34  adjustment=2
n=46  solutions=1402  difficulty=30  adjustment=-4
n=47  solutions=2100  difficulty=32  adjustment=2
n=48  solutions=2010  difficulty=34  adjustment=2
n=49  solutions=1402  difficulty=30  adjustment=-4
n=50  solutions=2100  difficulty=32  adjustment=2
--------------------------------------------------------
```

The effect of this is even more chaotic at higher difficulties.

### Solutions

A difficulty based on a linear scale or nBits would alleviate this issue. Understandably, this is
not trivial and requires a moderate amount of change to the codebase and possibly the block
structures (since the difficulty is currently represented as a `uint8_t`).

From that point onwards, a tested difficulty adjustment algorithm could be selected. For an
introduction on some of the difficulty algorithms used in privacy coins, the following repository
can be referenced: https://github.com/zawy12/difficulty-algorithms/issues/12.


## Results

```
# python difficulty.py
Global hashrate required to maintain 1810 nodes:
Diff 00 =       10 H/s
Diff 01 =       20 H/s
Diff 02 =       40 H/s
Diff 03 =       81 H/s
Diff 04 =      162 H/s
Diff 05 =      325 H/s
Diff 06 =      650 H/s
Diff 07 =       1 Kh/s
Diff 08 =       3 Kh/s
Diff 09 =       5 Kh/s
Diff 10 =      10 Kh/s
Diff 11 =      21 Kh/s
Diff 12 =      42 Kh/s
Diff 13 =      83 Kh/s
Diff 14 =     167 Kh/s
Diff 15 =     333 Kh/s
Diff 16 =     666 Kh/s
Diff 17 =       1 Mh/s
Diff 18 =       3 Mh/s
Diff 19 =       5 Mh/s
Diff 20 =      11 Mh/s
Diff 21 =      21 Mh/s
Diff 22 =      43 Mh/s
Diff 23 =      85 Mh/s
Diff 24 =     171 Mh/s
Diff 25 =     341 Mh/s
Diff 26 =     682 Mh/s
Diff 27 =       1 Gh/s
Diff 28 =       3 Gh/s
Diff 29 =       5 Gh/s
Diff 30 =      11 Gh/s
Diff 31 =      22 Gh/s
Diff 32 =      44 Gh/s
Diff 33 =      87 Gh/s
Diff 34 =     175 Gh/s
Diff 35 =     349 Gh/s
Diff 36 =     699 Gh/s
Diff 37 =       1 Th/s
Diff 38 =       3 Th/s
Diff 39 =       6 Th/s
Diff 40 =      11 Th/s
Diff 41 =      22 Th/s
Diff 42 =      45 Th/s
Diff 43 =      89 Th/s
Diff 44 =     179 Th/s
Diff 45 =     358 Th/s
Diff 46 =     715 Th/s
Diff 47 =    1431 Th/s
Diff 48 =    2862 Th/s
Diff 49 =    5723 Th/s
--------------------------------------------------------


Simulating for 50 epochs:
Starting Difficulty: 32
Global Hashrate: 58 Gh/s
n=01  solutions=2010  difficulty=34  adjustment=2
n=02  solutions=1402  difficulty=29  adjustment=-4
n=03  solutions=2100  difficulty=31  adjustment=2
n=04  solutions=2100  difficulty=33  adjustment=2
n=05  solutions=1605  difficulty=31  adjustment=-2
n=06  solutions=2100  difficulty=33  adjustment=2
n=07  solutions=1605  difficulty=31  adjustment=-2
n=08  solutions=2100  difficulty=33  adjustment=2
n=09  solutions=1605  difficulty=31  adjustment=-2
n=10  solutions=2100  difficulty=33  adjustment=2
n=11  solutions=1605  difficulty=31  adjustment=-2
n=12  solutions=2100  difficulty=33  adjustment=2
n=13  solutions=1605  difficulty=31  adjustment=-2
n=14  solutions=2100  difficulty=33  adjustment=2
n=15  solutions=1605  difficulty=31  adjustment=-2
n=16  solutions=2100  difficulty=33  adjustment=2
n=17  solutions=1605  difficulty=31  adjustment=-2
n=18  solutions=2100  difficulty=33  adjustment=2
n=19  solutions=1605  difficulty=31  adjustment=-2
n=20  solutions=2100  difficulty=33  adjustment=2
n=21  solutions=1605  difficulty=31  adjustment=-2
n=22  solutions=2100  difficulty=33  adjustment=2
n=23  solutions=1605  difficulty=31  adjustment=-2
n=24  solutions=2100  difficulty=33  adjustment=2
n=25  solutions=1605  difficulty=31  adjustment=-2
n=26  solutions=2100  difficulty=33  adjustment=2
n=27  solutions=1605  difficulty=31  adjustment=-2
n=28  solutions=2100  difficulty=33  adjustment=2
n=29  solutions=1605  difficulty=31  adjustment=-2
n=30  solutions=2100  difficulty=33  adjustment=2
n=31  solutions=1605  difficulty=31  adjustment=-2
n=32  solutions=2100  difficulty=33  adjustment=2
n=33  solutions=1605  difficulty=31  adjustment=-2
n=34  solutions=2100  difficulty=33  adjustment=2
n=35  solutions=1605  difficulty=31  adjustment=-2
n=36  solutions=2100  difficulty=33  adjustment=2
n=37  solutions=1605  difficulty=31  adjustment=-2
n=38  solutions=2100  difficulty=33  adjustment=2
n=39  solutions=1605  difficulty=31  adjustment=-2
n=40  solutions=2100  difficulty=33  adjustment=2
n=41  solutions=1605  difficulty=31  adjustment=-2
n=42  solutions=2100  difficulty=33  adjustment=2
n=43  solutions=1605  difficulty=30  adjustment=-2
n=44  solutions=2100  difficulty=32  adjustment=2
n=45  solutions=2010  difficulty=34  adjustment=2
n=46  solutions=1402  difficulty=30  adjustment=-4
n=47  solutions=2100  difficulty=32  adjustment=2
n=48  solutions=2010  difficulty=34  adjustment=2
n=49  solutions=1402  difficulty=30  adjustment=-4
n=50  solutions=2100  difficulty=32  adjustment=2
--------------------------------------------------------


Simulating for 50 epochs:
Starting Difficulty: 40
Global Hashrate: 15 Th/s
n=01  solutions=2018  difficulty=42  adjustment=2
n=02  solutions=1404  difficulty=38  adjustment=-4
n=03  solutions=2100  difficulty=40  adjustment=2
n=04  solutions=2018  difficulty=42  adjustment=2
n=05  solutions=1404  difficulty=38  adjustment=-4
n=06  solutions=2100  difficulty=40  adjustment=2
n=07  solutions=2018  difficulty=42  adjustment=2
n=08  solutions=1404  difficulty=38  adjustment=-4
n=09  solutions=2100  difficulty=40  adjustment=2
n=10  solutions=2018  difficulty=42  adjustment=2
n=11  solutions=1404  difficulty=38  adjustment=-4
n=12  solutions=2100  difficulty=40  adjustment=2
n=13  solutions=2018  difficulty=42  adjustment=2
n=14  solutions=1404  difficulty=38  adjustment=-4
n=15  solutions=2100  difficulty=40  adjustment=2
n=16  solutions=2018  difficulty=42  adjustment=2
n=17  solutions=1404  difficulty=38  adjustment=-4
n=18  solutions=2100  difficulty=40  adjustment=2
n=19  solutions=2018  difficulty=42  adjustment=2
n=20  solutions=1404  difficulty=38  adjustment=-4
n=21  solutions=2100  difficulty=40  adjustment=2
n=22  solutions=2018  difficulty=42  adjustment=2
n=23  solutions=1404  difficulty=38  adjustment=-4
n=24  solutions=2100  difficulty=40  adjustment=2
n=25  solutions=2018  difficulty=42  adjustment=2
n=26  solutions=1404  difficulty=38  adjustment=-4
n=27  solutions=2100  difficulty=40  adjustment=2
n=28  solutions=2018  difficulty=42  adjustment=2
n=29  solutions=1404  difficulty=38  adjustment=-4
n=30  solutions=2100  difficulty=40  adjustment=2
n=31  solutions=2018  difficulty=42  adjustment=2
n=32  solutions=1404  difficulty=38  adjustment=-4
n=33  solutions=2100  difficulty=40  adjustment=2
n=34  solutions=2018  difficulty=42  adjustment=2
n=35  solutions=1404  difficulty=38  adjustment=-4
n=36  solutions=2100  difficulty=40  adjustment=2
n=37  solutions=2018  difficulty=42  adjustment=2
n=38  solutions=1404  difficulty=38  adjustment=-4
n=39  solutions=2100  difficulty=40  adjustment=2
n=40  solutions=2018  difficulty=42  adjustment=2
n=41  solutions=1404  difficulty=38  adjustment=-4
n=42  solutions=2100  difficulty=40  adjustment=2
n=43  solutions=2018  difficulty=42  adjustment=2
n=44  solutions=1404  difficulty=38  adjustment=-4
n=45  solutions=2100  difficulty=40  adjustment=2
n=46  solutions=2018  difficulty=42  adjustment=2
n=47  solutions=1404  difficulty=38  adjustment=-4
n=48  solutions=2100  difficulty=40  adjustment=2
n=49  solutions=2018  difficulty=42  adjustment=2
n=50  solutions=1404  difficulty=38  adjustment=-4
--------------------------------------------------------
```
