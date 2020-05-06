#!/usr/bin/python3
# coding: UTF-8

from typing import List
import numpy as np
import sys

class HubTipLineClass:
	def __init__(self,HubP,TipP):
		self.HubPoint : float = HubP
		self.TipPoint : float = TipP
		self.iHubPoint = -1 # hub point id. set it on the basis of nearest point.
		self.iTipPoint = -1

class BladeRowClass:
	def __init__(self,iRow,IGT,AAA,BBB,DBLD,inlet,outlet):
		self.iRow = iRow
		self.IGT  = IGT
		self.AAA  = AAA
		self.BBB  = BBB
		self.DBLD = DBLD
		self.inlet : HubTipLineClass = inlet
		self.outlet: HubTipLineClass = outlet

class geomInpClass:
	def __init__(self):
		self.i1   = 0
		self.i2   = 0
		self.NRow = 0
		self.IPOP = 0
		self.BladeRows : List[BladeRowClass] = []
		self.NumHubPt = 0
		self.NumTipPt = 0
		self.HubPoints = [] # X , Y , lineType(straight or spline)
		self.TipPoints = [] # X , Y , lineType(straight or spline)
		self.DivideLine : List[HubTipLineClass] = []

	def readGeomInp(self,fname):
		f = open(fname,'r')
		# Line 1
		line      = f.readline().rstrip('\n').split('=')[-1].split(',')
		self.i1   = int(line[0])
		self.i2   = int(line[1])
		# Line 2
		line      = f.readline().rstrip('\n').split('=')[-1]
		self.i3   = int(line)
		# Line 3
		line      = f.readline()
		# Line 4
		line      = f.readline().rstrip('\n').split('=')[-1]
		self.IPOP = int(line)
		# Line 5
		line      = f.readline().rstrip('\n').split('=')[-1]
		self.NRow = int(line)
		# Line 6
		line      = f.readline()

		# ---------------------
		# *** Read Row data ***
		# ---------------------
		for i in range(self.NRow):
			line = f.readline().split()
			IGT  = int(line[1])
			AAA  = int(line[2])
			BBB  = float(line[3])
			DBLD = int(line[4])

			if   DBLD == 99: # Dummy Blade
				line2= f.readline().split()
				HubPoint = list(map(float,line2[0:2]))
				TipPoint = list(map(float,line2[2:4]))
				inletLine = HubTipLineClass( HubPoint,TipPoint )

				line3      = f.readline().split()
				HubPoint = list(map(float,line3[0:2]))
				TipPoint = list(map(float,line3[2:4]))
				outletLine = HubTipLineClass( HubPoint,TipPoint )
			elif DBLD == 1:
				HubPoint   = [0.0,0.0]
				TipPoint   = [0.0,0.0]
				inletLine  = HubTipLineClass( HubPoint,TipPoint )
				outletLine = HubTipLineClass( HubPoint,TipPoint )
			else:
				print('Error: incompatible DBLD(now) :',DBLD)
				sys.exit()

			Blade = BladeRowClass( i+1,IGT,AAA,BBB,DBLD,inletLine,outletLine )
			self.BladeRows.append(Blade)

		line = f.readline()

		# ------------------------
		# *** Read points data ***
		# ------------------------
		line = f.readline().rstrip('\n').split('=')[-1].split(',')
		self.NumHubPt = int(line[0])
		self.NumTipPt = int(line[1])
		line = f.readline()

		# Hub data
		for i in range(self.NumHubPt):
			points = f.readline().split()
			points[0] = float(points[0])
			points[1] = float(points[1])
			points[2] = int  (points[2])
			self.HubPoints.append(points)
		line = f.readline()

		# Tip data
		for i in range(self.NumTipPt):
			points = f.readline().split()
			points[0] = float(points[0])
			points[1] = float(points[1])
			points[2] = int  (points[2])
			self.TipPoints.append(points)

		line = f.readline()
		line = f.readline()

		# --------------------------
		# *** Division line data ***
		# --------------------------
		for i in range(self.IPOP+1):
			line     = f.readline().split()
			HubPoint = list(map(float,line[0:2]))
			TipPoint = list(map(float,line[2:4]))
			divLine  = HubTipLineClass( HubPoint,TipPoint )
			self.DivideLine.append(divLine)

		# --------------------------------------------------
		# *** search nearest point data for Hub-Tip line ***
		# --------------------------------------------------
		HubXY = np.array ([ l[:2] for l in self.HubPoints ])
		TipXY = np.array ([ l[:2] for l in self.TipPoints ])
		# for Blade Row
		for iBR in self.BladeRows:
			if   iBR.DBLD == 99:
				pass
			elif iBR.DBLD == 1:
				continue
			else:
				print("Error: incompatible DBLD (now) : ",iBR.DBLD)
				sys.exit()

			HP1   = np.array(iBR.inlet.HubPoint)
			diff  = HP1 - HubXY
			dist2 = diff[:,0]**2 + diff[:,1]**2
			iBR.inlet.iHubPoint = np.argmin(dist2)

			TP1   = np.array(iBR.inlet.TipPoint)
			diff  = TP1 - TipXY
			dist2 = diff[:,0]**2 + diff[:,1]**2
			iBR.inlet.iTipPoint = np.argmin(dist2)

			HP1   = np.array(iBR.outlet.HubPoint)
			diff  = HP1 - HubXY
			dist2 = diff[:,0]**2 + diff[:,1]**2
			iBR.outlet.iHubPoint = np.argmin(dist2)

			TP1   = np.array(iBR.outlet.TipPoint)
			diff  = TP1 - TipXY
			dist2 = diff[:,0]**2 + diff[:,1]**2
			iBR.outlet.iTipPoint = np.argmin(dist2)

		# for Divide line
		for iLine in self.DivideLine:
			HP1   = np.array(iLine.HubPoint)
			diff  = HP1 - HubXY
			dist2 = diff[:,0]**2 + diff[:,1]**2
			iLine.iHubPoint = np.argmin(dist2)

			TP1   = np.array(iLine.TipPoint)
			diff  = TP1 - TipXY
			dist2 = diff[:,0]**2 + diff[:,1]**2
			iTP   = np.argmin(dist2) 
			iLine.iTipPoint = np.argmin(dist2)

		f.close()

	def outputGeomInp(self,fname):
		# Introduction
		f = open(fname,'w')
		f.write('#dlfkjeirwoedlkjf lsdfje =    %d, %d\n' % (self.i1,self.i2))
		f.write('# dlfkwoedlkjf- lsdfje = %d\n' % (self.i3))
		f.write('#djfie\n')
		f.write('# IPOP = %d\n' % (self.IPOP))
		f.write('# NROW = %d\n' % (self.NRow))
		f.write('\n')

		# Blade Row
		for iBR in self.BladeRows:
			f.write('%d %d %d %f %d\n' % (iBR.iRow,iBR.IGT,iBR.AAA,iBR.BBB,iBR.DBLD))
			#print(iBR.inlet.HubPoint)
			if iBR.DBLD == 99:
				print(iBR.inlet.TipPoint[0])
				print(iBR.inlet.TipPoint[1])
				f.write(' %f %f %f %f \n' % (iBR.inlet.HubPoint [0] ,iBR.inlet.HubPoint [1], \
				                             iBR.inlet.TipPoint [0] ,iBR.inlet.TipPoint [1] ))
				f.write(' %f %f %f %f \n' % (iBR.outlet.HubPoint[0] ,iBR.outlet.HubPoint[1], \
				                             iBR.outlet.TipPoint[0] ,iBR.outlet.TipPoint[1] ))
		f.write('\n')

		# Points
		f.write('#points   =%d ,%d\n' %(self.NumHubPt,self.NumTipPt) )
		f.write('#hub\n')
		for iHub in self.HubPoints:
			f.write('%f %f %d\n' % (iHub[0],iHub[1],iHub[2]))

		f.write('#tip\n')
		for iTip in self.TipPoints:
			f.write('%f %f %d\n' % (iTip[0],iTip[1],iTip[2]))

		f.write('\n')
		f.write('# inlet outlet\n')
		for iDivLine in self.DivideLine:
			f.write('%f %f %f %f\n' % (iDivLine.HubPoint[0],iDivLine.HubPoint[1], \
			                           iDivLine.TipPoint[0],iDivLine.TipPoint[1]  ))

	def correctGassPath(self,PathFname):
		# -----------------------------
		# *** Read correctCurve.dat ***
		# -----------------------------
		f = open(PathFname,'r')
		line = f.readline()
		line = f.readline().split()
		targetDivSt     = int(line[0])
		targetDivStType = int(line[1])
		line = f.readline()

		line = f.readline()
		line = f.readline().split()
		targetDivEd     = int(line[0])
		targetDivEdType = int(line[1])
		line = f.readline()

		line = f.readline()
		line = f.readline().split()
		NumHubCor = int(line[0])
		NumTipCor = int(line[1])
		line = f.readline()

		line = f.readline()
		HubPtCor  = []
		for i in range(NumHubCor):
			line = f.readline().split()
			Pt   = list(map(float,line[0:2]))
			Pt.append( int(line[2]) )
			HubPtCor.append(Pt)
		line = f.readline()
		line = f.readline()

		TipPtCor  = []
		for i in range(NumTipCor):
			line = f.readline().split()
			Pt   = list(map(float,line[0:2]))
			Pt.append( int(line[2]) )
			TipPtCor.append(Pt)
		f.close()

		# ---------------
		# *** correct ***
		# ---------------
		iHubPtSt = self.DivideLine[targetDivSt].iHubPoint
		iHubPtEd = self.DivideLine[targetDivEd].iHubPoint
		iTipPtSt = self.DivideLine[targetDivSt].iTipPoint
		iTipPtEd = self.DivideLine[targetDivEd].iTipPoint

		# correct HubPoint
		if   targetDivStType == 0:
			r1 = iHubPtSt
		elif targetDivStType == 1: 
			r1 = iHubPtSt+1

		if   targetDivEdType == 0:
			r2 = iHubPtEd+1
		elif targetDivEdType == 1: 
			r2 = iHubPtEd

		del self.HubPoints[r1:r2]
		#self.HubPoints.append(HubPtCor)
		self.HubPoints[r1:0] = HubPtCor
		print(self.HubPoints)

		# correct TipPoint
		if   targetDivStType == 0:
			r1 = iTipPtSt
		elif targetDivStType == 1: 
			r1 = iTipPtSt+1

		if   targetDivEdType == 0:
			r2 = iTipPtEd+1
		elif targetDivEdType == 1: 
			r2 = iTipPtEd

		del self.TipPoints[r1:r2]
		self.TipPoints[r1:0] = TipPtCor
		#self.TipPoints.append(TipPtCor)

		self.NumHubPt = len(self.HubPoints)
		self.NumTipPt = len(self.TipPoints)

def main():
	geomInp1 = geomInpClass()
	geomInp1.readGeomInp('geom.data')

	geomInp2 = geomInp1
	geomInp2.correctGassPath('correctCurve.dat')
	geomInp2.outputGeomInp('geom_new.data')

if __name__ == "__main__":
	main()
