# 演算法分析機測
# 學號 : 10827114 / 10827129 / 10827141
# 姓名 : 盧俊崴 / 周暐倫 / 楊睿真
# 中原大學資訊工程系

import cv2
import os
import random
import bisect
import heapq
import matplotlib.pyplot as plt
import numpy as np
from operator import attrgetter


class PlotWindow:
    WINDOW_SIZE = (960, 540)

    def __init__(self, image, title = ''):
        fig = plt.figure( figsize = (8, 8 * (image.shape[0] / image.shape[1])))
        ax = plt.Axes(fig, [0., 0., 1., .9])
        fig.add_axes(ax)
        self.data = ax.imshow(image)
        self.Draw(image, title)

    def Draw(self, image, title = ''):
        self.data.set_data( image )
        plt.suptitle( title )
        plt.draw()
        plt.pause( 0.1 )
# -------------- End Of class PlotWindow ------------------


class GeneticAlgorithm:
    def __init__(self, Piece, Row, Column) -> None :
        self.pieces, self.row, self.col = Piece, Row, Column
        self.solutions = [PuzzleSolution(Piece, Row, Column) for a in range(200)]

    def evolution(self):
        returnSolution, maxFitness, terminationCount = None, -int(1e9 + 7), 0

        for a in range(20) :
            newSolution = []
            newSolution.extend( sorted(self.solutions, key = attrgetter("fitness"))[-2:] )
            selectedSols = self.rouletteSelection(self.solutions, 198)

            for firstSol, secondSol in selectedSols:
                crossover = Crossover(firstSol, secondSol)
                crossover.run()
                newSolution.append(crossover.child())

            fittest = max(self.solutions, key = attrgetter("fitness"))

            if fittest.getFitness() <= maxFitness :
                terminationCount += 1
            else:
                maxFitness = fittest.getFitness()
                returnSolution = fittest

            plot.Draw( returnSolution.toImage() )
            self.solutions = newSolution

        return returnSolution

    def rouletteSelection(self, sample, num):
        allSum = 0
        fitnessValues = [x.getFitness() for x in sample]
        preSum = []

        for x in fitnessValues:
            allSum += x
            preSum.append(allSum)

        res = []
        for i in range(num):
            res.append((sample[bisect.bisect_left(preSum, random.uniform(0, preSum[-1]))], sample[bisect.bisect_left(preSum, random.uniform(0, preSum[-1]))]))

        return res
# -------------- End Of class GeneticAlgorithm ------------------


class Crossover:

    def __init__(self, firstParent, secondParent) -> None:
        self.parent = (firstParent, secondParent)
        self.row, self.col = firstParent.row, firstParent.col
        self.maxRow, self.minRow, self.maxCol, self.minCol = 0, 0, 0, 0
        self.kernel = [None for i in range(firstParent.size())]
        self.vis = set()
        self.pQueue = []

    def initKernel(self):
        self.addToKernel(self.parent[0].pieces[int(random.uniform(0, self.parent[0].size()))].id, (0, 0))

    def run(self):
        self.initKernel()
        while (len(self.pQueue)):
            _, (pieceId, pos), rest_dir = heapq.heappop(self.pQueue)
            if pos in self.vis:
                continue

            if self.kernel[pieceId] is not None:
                self.addToQueue(rest_dir[0], rest_dir[1], pos)
                continue

            self.addToKernel(pieceId, pos)

    def child(self):
        res = [None for i in range(self.parent[0].size())]
        for pieceId, (y, x) in enumerate(self.kernel):
            res[(y - self.minRow) * self.col + x - self.minCol] = self.parent[0].getPieceById(pieceId)
        return PuzzleSolution(res, self.row, self.col, False)

    def addToKernel(self, pieceId, pos):
        self.kernel[pieceId] = pos
        self.vis.add(pos)
        self.updateQueue(pieceId, pos)

    def updateQueue(self, pieceId, pos):
        for dir, nextPos in self.getValidPos(pos):
            self.addToQueue(pieceId, dir, nextPos)

    def addToQueue(self, pieceId, dir, pos):
        if self.isValidPieceId(self.getSharedPiece(pieceId, dir)):
            self.addSharedPiece(self.getSharedPiece(pieceId, dir), pos, (pieceId, dir))
            return

        if self.isValidPieceId(self.getBuddyPiece(pieceId, dir)):
            self.addBuddyPiece(self.getBuddyPiece(pieceId, dir), pos, (pieceId, dir))
            return

        dissimilarity, fittestPiece = self.getFittestPiece(pieceId, dir)
        if self.isValidPieceId(fittestPiece):
            self.addFittestPiece(dissimilarity, fittestPiece, pos, (pieceId, dir))
            return

    def isValidPieceId(self, pieceId):
        return pieceId is not None and self.kernel[pieceId] is None

    def getSharedPiece(self, pieceId, dir):
        f, s = self.parent
        if f.edge(pieceId, dir) == s.edge(pieceId, dir) :
            return f.edge(pieceId, dir)

    def getBuddyPiece(self, pieceId, dir):
        firstBuddy  = ImageAnalysis.getBestMatch(pieceId, dir)
        secondBuddy = ImageAnalysis.getBestMatch(firstBuddy, (dir + 2) % 4)

        if secondBuddy == pieceId :
            for x in [p.edge(pieceId, dir) for p in self.parent]:
                if x == firstBuddy:
                    return x

    def getFittestPiece(self, pieceId, dir):
        for x in ImageAnalysis.bestMatchList[pieceId][dir]:
            if self.kernel[x[1]] is None:
                return x

    def addSharedPiece(self, pieceId, pos, rest_dir):
        heapq.heappush(self.pQueue, (-10, (pieceId, pos), rest_dir))

    def addBuddyPiece(self, pieceId, pos, rest_dir):
        heapq.heappush(self.pQueue, (-1., (pieceId, pos), rest_dir))

    def addFittestPiece(self, weight, pieceId, pos, rest_dir):
        heapq.heappush(self.pQueue, (weight, (pieceId, pos), rest_dir))

    def getValidPos(self, pos):
        res = []
        y, x = pos
        for a in range(4):
            nextPos = (y + [0, 1, 0, -1, 0][a], x + [0, 1, 0, -1, 0][a + 1])
            if nextPos not in self.vis and self.inKernelRange(nextPos):
                res.append((a, nextPos))
                self.updateBoundary(nextPos)

        return res

    def updateBoundary(self, pos):
        y, x = pos
        self.minCol, self.minRow = min(self.minCol, x), min(self.minRow, y)
        self.maxCol, self.maxRow = max(self.maxCol, x), max(self.maxRow, y)

    def inKernelRange(self, pos):
        y, x = pos
        return self.inKernelRowRange(y) and self.inKernelColRange(x)

    def inKernelRowRange(self, y):
        return abs(min(self.minRow, y)) + abs(max(self.maxRow, y)) < self.row

    def inKernelColRange(self, x):
        return abs(min(self.minCol, x)) + abs(max(self.maxCol, x)) < self.col
# -------------- End Of class Crossover ------------------


class Image:
    def __init__(self, img, id = None) -> None:
        self.img, self.id = img, id

    def __getitem__(self, index):
        return self.img.__getitem__(index)

    def edge(self, dir):
        if dir == 0:
            return self.img[:, -1]
        elif dir == 1:
            return self.img[-1]
        elif dir == 2:
            return self.img[:, 0]
        elif dir == 3:
            return self.img[0]
# -------------- End Of class Image ------------------


class ImageHelper:
    @staticmethod
    def flattenImage(image, imageEdgeLen):
        height, width = image.shape[:2]
        row, column = height // imageEdgeLen, width // imageEdgeLen
        res = []
        id = 0
        for i in range(0, height, imageEdgeLen):
            for j in range(0, width, imageEdgeLen):
                temp = np.empty((imageEdgeLen, imageEdgeLen, image.shape[2]))
                temp[::] = image[i : i + imageEdgeLen, j : j + imageEdgeLen]
                res = np.append(res, Image(temp, id))
                id += 1

        return np.array(res), row, column

    @staticmethod
    def assembleImage(images, row, column):
        res = []
        for a in range(row):
            columnList = []

            for b in range(column):
                columnList.append(images[a * column + b])

            res.append(np.hstack(columnList))

        return np.vstack(res).astype(np.uint8)
# -------------- End Of class ImageHelper ------------------


class ImageAnalysis:
    bestMatchList = []
    dissimilarityList = []

    @classmethod
    def analysis(cls, pieces):
        n = len(pieces)
        cls.bestMatchList = [[[] for a in range(4)] for b in range(n)]
        cls.dissimilarityList = [[[None for a in range(2)] for b in range(n)] for c in range(n)]

        def update(firstPiece, secondPiece, dir):
            revDir = (dir + 2) % 4
            dissimilarity = cls.calcDissimilarityValue(firstPiece.edge(dir), secondPiece.edge(revDir))
            cls.dissimilarityList[firstPiece.id][secondPiece.id][dir] = dissimilarity
            cls.bestMatchList[firstPiece.id][dir].append((dissimilarity, secondPiece.id))
            cls.bestMatchList[secondPiece.id][revDir].append((dissimilarity, firstPiece.id))

        for a in range(n):
            for b in range(a + 1, n):
                for c in range(2):
                    update(pieces[a], pieces[b], c)
                    update(pieces[b], pieces[a], c)

        for a in range(n):
            for b in range(4):
                cls.bestMatchList[a][b].sort(key = lambda x : x[0])


    def calcDissimilarityValue(first, second):
        return np.sum((first - second) * (first - second))

    @classmethod
    def getBestMatch(cls, rest, dir):
        return cls.bestMatchList[rest][dir][0][1]

    @classmethod
    def getDissimilarity(cls, rest, dist, dir):
        return cls.dissimilarityList[rest][dist][dir]
# -------------- End Of class ImageAnalysis ------------------


class PuzzleSolution:
    def __init__(self, pieces, row, col, shuffle = True) -> None :
        self.pieces = pieces.copy()
        self.row, self.col, self.fitness = row, col, 0
        if shuffle:
            random.shuffle(self.pieces)
        self.pieceId_index = { x.id : i for i, x in enumerate(self.pieces) }
        self.calcFitness()

    def calcFitness(self):
        for a in range(self.row):
            for b in range(self.col - 1):
                self.fitness += ImageAnalysis.getDissimilarity(self.pieces[a * self.col + b].id, self.pieces[a * self.col + b + 1].id, 0)

        for a in range(self.row - 1):
            for b in range(self.col):
                self.fitness += ImageAnalysis.getDissimilarity(self.pieces[a * self.col + b].id, self.pieces[(a + 1) * self.col + b].id, 1)

        self.fitness = int(1e9 + 7) / self.fitness

    def getFitness(self):
        return self.fitness

    def size(self):
        return len(self.pieces)

    def edge(self, pieceId, dir):
        idx = (self.pieceId_index[pieceId] // self.col +[0, 1, 0, -1, 0][dir]) * self.col + self.pieceId_index[pieceId] % self.col +[0, 1, 0, -1, 0][dir + 1]
        if 0 <= idx and idx < self.size() :
            return self.pieces[idx].id

    def getPieceById(self, pieceId):
        return self.pieces[ self.pieceId_index[pieceId]]

    def toImage(self):
        return ImageHelper.assembleImage([x.img for x in self.pieces], self.row, self.col)
# -------------- End Of class PuzzleSolution ------------------


class Roller:
    @staticmethod
    def rollToFittest(sol, row, column):
        maxFitness = -int(1e9 + 7)
        res = None
        rolledPieces = np.reshape(sol.pieces, (row, column))

        def update(pieces):
            nonlocal maxFitness, res
            ps = PuzzleSolution(pieces, row, column, False)
            if ps.getFitness() > maxFitness:
                res = ps
                maxFitness = ps.getFitness()

        for a in range(row):
            flattenRolledPieces = rolledPieces.flatten()
            update(flattenRolledPieces)

            for b in range(column):
                rolledPieces = np.roll(rolledPieces, 1, axis = 1)
                flattenRolledPieces = rolledPieces.flatten()
                update(flattenRolledPieces)

            rolledPieces = np.roll(rolledPieces, 1, axis = 0)

        return res
# -------------- End Of class Roller ------------------


path = input('Please enter an image file : ')
os.chdir(os.path.dirname(os.path.abspath(__file__)))
image = cv2.imread(path)[:, :, ::-1] # BGR -> RGB
plot = PlotWindow(image)
splitImage, row, column = ImageHelper.flattenImage(image, 120)
ImageAnalysis.analysis(splitImage)

final = GeneticAlgorithm(splitImage, row, column)
cv2.imwrite(path.split('.')[0] + '_result.bmp', final.evolution().toImage()[:, :, ::-1])  # RGB -> BGR
cv2.waitKey(0)