import math
import time

def nonogram_solve():
	dimxdimxdim=raw_input("Enter puzzle dimension, col x row x colors, e.g. 8x4x3  ")
	dims = dimxdimxdim.split("x")
	num_cols = int(dims[0])
	num_rows = int(dims[1])
	num_colors = int(dims[2])
	cols=[]
	rows=[]
	flatcols=[]
	flatrows=[]
	iteration_times=[]

	rows_flatrows=read_rows(num_rows,"horiz","vert","row")
	rows=rows_flatrows[0]
	flatrows=rows_flatrows[1]

	cols_flatcols=read_rows(num_cols,"vert","","col")
	cols=cols_flatcols[0]
	flatcols=cols_flatcols[1]

	total_start_time=time.time()

	colors=checkinputs(flatrows,flatcols)
	
	print(rows)
	print(cols)
	print(colors)
	truegrid=[]
	xtruegrid=[]
	for r in rows:
		newrow='.'*num_cols
		truegrid.append(newrow)

	spacelist=build_spacelist(rows,num_cols)
	xspacelist=build_spacelist(cols,num_rows)

	count_to=10	
	count=1	
	dummy="continue"
	last_dot_count=num_rows*num_cols
	possibles_c=[]
	while dummy=="continue":
		## solve based on rows
		iter_start=time.time()
		print("start iteration "+str(count))
		print("simple rows")
		tg_sl = simple_rowcheck(truegrid,spacelist,rows)
		truegrid=tg_sl[0]
		spacelist=tg_sl[1]
		print("rows done")
		## transfer truegrid into xtruegrid
		xtruegrid=transpose_grid(truegrid,num_cols)

		sp=show_progress(truegrid,last_dot_count)
		solved=sp[0]
		last_dot_count=sp[1]

		## solve based on columns
		## i.e. same shit, but for xtruegrid
		print("simple columns")
		tg_sl = simple_rowcheck(xtruegrid,xspacelist,cols)
		xtruegrid=tg_sl[0]
		xspacelist=tg_sl[1]
		print("cols done")		
		## transfer xtruegrid back into truegrid		
		truegrid=transpose_grid(xtruegrid,num_rows)	

		sp=show_progress(truegrid,last_dot_count)
		solved=sp[0]
		last_dot_count=sp[1]
		
		print("simple color possibles cross")
		possibles_r = color_possibles(truegrid,spacelist,rows,xspacelist,cols)
		if len(possibles_c)==0:
			possibles_c = color_possibles(xtruegrid,xspacelist,cols,spacelist,rows)
		truegrid = cross_possibles(possibles_r,possibles_c,colors)
		xtruegrid = transpose_grid(truegrid,num_cols)
		
		sp=show_progress(truegrid,last_dot_count)
		solved=sp[0]
		last_dot_count=sp[1]
		
		possibles_c = color_possibles(xtruegrid,xspacelist,cols,spacelist,rows)
		xtruegrid = cross_possibles(possibles_c,possibles_r,colors)
		truegrid = transpose_grid(xtruegrid,num_rows)

		sp=show_progress(truegrid,last_dot_count)
		solved=sp[0]
		last_dot_count=sp[1]

		## cross check simples against possibles
		print("rows vs. column possibles")
		tg_sl = simple_rowcheck(truegrid,spacelist,rows,possibles_c,colors)
		truegrid=tg_sl[0]
		spacelist=tg_sl[1]
		xtruegrid=transpose_grid(truegrid,num_cols)

		sp=show_progress(truegrid,last_dot_count)
		solved=sp[0]
		last_dot_count=sp[1]

		print("columns vs. row possibles")
		tg_sl = simple_rowcheck(xtruegrid,xspacelist,cols,possibles_r,colors)
		xtruegrid=tg_sl[0]
		xspacelist=tg_sl[1]
		truegrid=transpose_grid(xtruegrid,num_rows)	


		sp=show_progress(truegrid,last_dot_count)
		solved=sp[0]
		last_dot_count=sp[1]
		print("end iteration "+str(count))
		if solved:
			dummy="stop"
		elif count>=count_to:		
			change_dummy=raw_input("enter STOP to stop  ")
			if change_dummy=="STOP":dummy="stop"
		count+=1		
		iter_end=time.time()
		iter_elapsed=iter_end-iter_start
		print(str(iter_elapsed)+" secs this iteration")
		iteration_times.append(iter_elapsed)
	
	print(rows)
	print(cols)
	print(truegrid)
	total_end_time=time.time()
	total_elapsed=total_end_time-total_start_time
	print (iteration_times)
	print (str(total_elapsed)+" seconds total")


def check_inputs(flatcols,flatrows,colors):
	for c in flatcols:
		lc=len(c)
		i=int(c[0:lc-1])
		color=c[lc-1]

def transpose_grid(source_grid,num_cols):
	target_grid=[]
	for cn in range(num_cols):
		temp=''
		for r in source_grid:
			temp = temp+r[cn:cn+1]
		target_grid.append(temp)
	return target_grid

def simple_rowcheck(truegrid,spacelist,rows,possibles_c=[],colors=[]):
	start_time=time.time()
	num_rows=len(rows)
	num_cols=len(truegrid[0])
	for r in range(num_rows):
		st=time.time()
		row=rows[r]
		blocks=len(row)
		tgrow=truegrid[r]
		## build potential rows
		potential_rows=[]
		slremove=[]
		for potential_space in spacelist[r]:
			##slremove=[]
			potential_row=''
			last_color='.'
			for b in range(blocks):
				for x in range(potential_space[b]):
					potential_row=potential_row+" "
				ic=row[b]
				lic=len(ic)
				i=int(ic[0:lic-1])
				c=ic[lic-1:]
				if c==last_color:
					potential_row=potential_row+" "
				for x in range(i):
					potential_row=potential_row+c
				last_color=c
			trailing_spaces=num_cols-len(potential_row)
			for x in range(trailing_spaces):
				potential_row=potential_row+" "
			## potential_row complete.  Check against truegrid.
			truegrid_check=True
			for x in range(len(potential_row)):
				if (tgrow[x:x+1]!='.') and (potential_row[x:x+1]!=tgrow[x:x+1]):
					truegrid_check=False
				if len(possibles_c)>0 and (potential_row[x:x+1] not in possibles_c[x][r]):
					truegrid_check=False
			if truegrid_check:
				potential_rows.append(potential_row)
			else:
				slremove.append(potential_space)
		remove_len=len(slremove)
		for x in slremove:
			spacelist[r].remove(x)
		## potential rows are built			
		## find features common to all potential rows
		newtrue=''
		for x in range(num_cols):
			newtrue=newtrue+potential_rows[0][x:x+1]
		for pr in potential_rows:
			for x in range(num_cols):
				if newtrue[x:x+1]!=pr[x:x+1]:newtrue=newtrue[0:x]+'.'+newtrue[x+1:]
		if newtrue!='':
			truegrid[r]=newtrue	
		et=time.time()
		elap=et-st
		print(str(r)+"    "+str(elap)+ "sec   " +str(remove_len)+ " removed")
	end_time=time.time()
	elapsed_secs=end_time-start_time
	return [truegrid,spacelist,elapsed_secs]

def color_possibles(truegrid,spacelist,rows,xspacelist,cols):
	num_rows=len(rows)
	num_cols=len(truegrid[0])
	#write possibles
	possibles=[]
	for r in range(num_rows):
		row=truegrid[r]
		possibles.append([])
		lr=len(row)
		for cn in range(lr):
			possibles[r].append([])
			possibles[r][cn].append(truegrid[r][cn:cn+1])
	for r in range(num_rows):
		row=rows[r]
		blocks=len(row)
		tgrow=truegrid[r]
		## build potential rows
		potential_rows=[]
		for potential_space in spacelist[r]:
			slremove=[]
			potential_row=''
			last_color='*'
			for b in range(blocks):
				for x in range(potential_space[b]):
					potential_row=potential_row+" "
				ic=row[b]
				lic=len(ic)
				i=int(ic[0:lic-1])
				c=ic[lic-1:]
				if c==last_color:
					potential_row=potential_row+" "
				for x in range(i):
					potential_row=potential_row+c
				last_color=c
			trailing_spaces=num_cols-len(potential_row)
			for x in range(trailing_spaces):
				potential_row=potential_row+" "
			## potential_row complete.  Check against truegrid.
			truegrid_check=True
			for x in range(len(potential_row)):
				if (tgrow[x:x+1]!='.') and (potential_row[x:x+1]!=tgrow[x:x+1]):
					truegrid_check=False
			if truegrid_check:
				potential_rows.append(potential_row)
			else:
				##spacelist[r].remove(potential_space)
				slremove.append(potential_space)
		for x in slremove:
			spacelist[r].remove(x)
		## potential rows are built			
		
		## append all possible values from potential_rows[r] to proper indices of possibles[r]
		for cn in range(num_cols):
			if possibles[r][cn][0]=='.':
				## if '.', then value is still unknown, so check and append possibles
					for pr in potential_rows:
						color=pr[cn:cn+1]
						if color not in possibles[r][cn]:
							possibles[r][cn].append(color)
	return possibles

def cross_possibles(possibles_r,possibles_c,colors):
	num_rows=len(possibles_r)
	num_cols=len(possibles_c)
	for r in range(num_rows):
		for cn in range(num_cols):
			## compare pr[r][cn] to pc[cn][r]
			if possibles_r[r][cn][0]==".":
				pr_remove=[]
				for x in range(1,len(possibles_r[r][cn])):
					color=possibles_r[r][cn][x]
					if color not in possibles_c[cn][r]:
						pr_remove.append(color)
				for color in pr_remove:
					if color in possibles_r[r][cn]:
						possibles_r[r][cn].remove(color)
			if possibles_c[cn][r][0]==".":
				pc_remove=[]
				for x in range(1,len(possibles_c[cn][r])):
					color=possibles_c[cn][r][x]
					if color not in possibles_r[r][cn]:
						pc_remove.append(color)
				for color in pc_remove:
					possibles_c[cn][r].remove(color)
			if len(possibles_r[r][cn])==2:
				if possibles_r[r][cn][0]==".":
					possibles_r[r][cn].remove(".")
	## define truegrid
	truegrid=[]
	for r in range(num_rows):
		newline=''
		for cn in range(num_cols):
			if len(possibles_r[r][cn])==1:
				newline=newline+possibles_r[r][cn][0]
			else:
				newline=newline+"."
		truegrid.append(newline)
	return truegrid

def color_gridcheck1(truegrid,spacelist,rows,xspacelist,cols):
	num_rows=len(rows)
	num_cols=len(truegrid[0])
	#write possibles
	possibles=[]
	for r in range(num_rows):
		row=truegrid[r]
		possibles.append([])
		lr=len(row)
		for cn in range(lr):
			possibles[r].append([])
			possibles[r][cn].append(truegrid[r][cn:cn+1])
	for r in range(num_rows):
		row=rows[r]
		blocks=len(row)
		tgrow=truegrid[r]
		## build potential rows
		potential_rows=[]
		for potential_space in spacelist[r]:
			slremove=[]
			potential_row=''
			last_color='*'
			for b in range(blocks):
				for x in range(potential_space[b]):
					potential_row=potential_row+" "
				ic=row[b]
				lic=len(ic)
				i=int(ic[0:lic-1])
				c=ic[lic-1:]
				if c==last_color:
					potential_row=potential_row+" "
				for x in range(i):
					potential_row=potential_row+c
				last_color=c
			trailing_spaces=num_cols-len(potential_row)
			for x in range(trailing_spaces):
				potential_row=potential_row+" "
			## potential_row complete.  Check against truegrid.
			truegrid_check=True
			for x in range(len(potential_row)):
				if (tgrow[x:x+1]!='.') and (potential_row[x:x+1]!=tgrow[x:x+1]):
					truegrid_check=False
			if truegrid_check:
				potential_rows.append(potential_row)
			else:
				##spacelist[r].remove(potential_space)
				slremove.append(potential_space)
		for x in slremove:
			spacelist[r].remove(x)
			
		## potential rows are built			
		## append all possible values from potential_rows[r] to proper indices of possibles[r]
		
		for cn in range(num_cols):
			if possibles[r][cn][0]=='.':
				## if '.', then value is still unknown, so check and append possibles
					for pr in potential_rows:
						color=pr[cn:cn+1]
						if color not in possibles[r][cn]:
							possibles[r][cn].append(color)
	xtruegrid=transpose_grid(truegrid,num_cols)
	for cn in range(num_cols):
		col=cols[cn]
		blocks=len(col)
		xtgcol=xtruegrid[cn]
		## build potential cols
		potential_cols=[]
		for potential_space in xspacelist[cn]:
			slremove=[]
			potential_col=''
			last_color='*'
			for b in range(blocks):
				for x in range(potential_space[b]):
					potential_col=potential_col+" "
				ic=col[b]
				lic=len(ic)
				i=int(ic[0:lic-1])
				c=ic[lic-1:]
				if c==last_color:
					potential_col=potential_col+" "
				for x in range(i):
					potential_col=potential_col+c
				last_color=c
			trailing_spaces=num_rows-len(potential_col)
			for x in range(trailing_spaces):
				potential_col=potential_col+" "
			## potential_col complete.  Check against xtruegrid.
			xtruegrid_check=True
			for x in range(len(potential_col)):
				if (xtgcol[x:x+1]!='.') and (potential_col[x:x+1]!=xtgcol[x:x+1]):
					xtruegrid_check=False
			if xtruegrid_check:
				potential_cols.append(potential_col)
			else:
				##spacelist[r].remove(potential_space)
				slremove.append(potential_space)
		for x in slremove:
			xspacelist[cn].remove(x)
		
		## potential cols are built
		
		## append all possible values from potential_cols[r] to proper indices of possibles[r]
		
		for r in range(num_rows):
			if possibles[r][cn][0]=='.':
				## if '.', then value is still unknown, so check and append possibles
					for pc in potential_cols:
						color=pc[r:r+1]
						if color not in possibles[r][cn]:
							possibles[r][cn].append(color)
	return [truegrid,spacelist]

def build_spacelist(rows,num_cols):
	num_rows=len(rows)
	spacelist=[]
	for r in range(num_rows):
		start_time=time.time()
		row=rows[r]
		##tgrow=truegrid[r]
		## build space list
		blocks=len(row)
		blocksum=0
		same_color_dividers=0
		last_color='.'
		## this could use some explicit zero row handling
		for ic in row:
			lic=len(ic)
			i=int(ic[0:lic-1])
			c=ic[lic-1:]
			blocksum+=i
			if c==last_color: same_color_dividers+=1
			last_color=c
		spaces=num_cols-(blocksum+same_color_dividers)
		calced=choose(spaces+blocks,spaces)
		print(calced)
		# if calced<100000:
			# spacelist.append(space_recurse(spaces+1,blocks-1))
		# else:
			# spacelist.append()
		spacelist.append(space_recurse(spaces+1,blocks-1))
		end_time=time.time()
		elapsed=end_time-start_time
		print(str(len(spacelist[r])) + "   " + str(elapsed) + " sec")
		
		## space list is built.
	return spacelist

def read_rows(num_rows,skipcode,earlycode,row_or_col):
	rows=[]
	flatrows=[]
	for r in range(num_rows):
		row=raw_input("Enter "+row_or_col+", e.g. 1g 3g 1h 2g  ")
		if row==skipcode:
			row=raw_input("Enter "+row_or_col+", e.g. 1g 3g 1h 2g  ")
		if row==earlycode:
			print("input error:  not enough "+row_or_col+"s")
		row_parse=row.split(" ")
		rows.append(row_parse)
		for r2 in range(len(row_parse)):
			flatrows.append(row_parse[r2])
	return [rows,flatrows]

def space_recurse(max_space,blocks):
	if blocks==0:
		step_list=[]
		for x in range(max_space):
			step_list.append([x])
	else:
		step_list=[]
		for x in range(max_space):
			new_list=space_recurse(max_space-x,blocks-1)
			for y in new_list:
				interim=[x]
				for z in range(len(y)):
					interim.append(y[z])
				step_list.append(interim)
	return step_list

def simple_vs_possibles(truegrid,spacelist,rows,possibles_c,colors):
	num_rows=len(rows)
	num_cols=len(truegrid[0])
	for r in range(num_rows):
		print(r)
		row=rows[r]
		blocks=len(row)
		tgrow=truegrid[r]
		## build potential rows
		potential_rows=[]
		slremove=[]
		for potential_space in spacelist[r]:
			potential_row=''
			last_color='.'
			for b in range(blocks):
				for x in range(potential_space[b]):
					potential_row=potential_row+" "
				ic=row[b]
				lic=len(ic)
				i=int(ic[0:lic-1])
				c=ic[lic-1:]
				if c==last_color:
					potential_row=potential_row+" "
				for x in range(i):
					potential_row=potential_row+c
				last_color=c
			trailing_spaces=num_cols-len(potential_row)
			for x in range(trailing_spaces):
				potential_row=potential_row+" "
			## potential_row complete.  Check against truegrid.
			truegrid_check=True
			for x in range(len(potential_row)):
				if (tgrow[x:x+1]!='.') and (potential_row[x:x+1]!=tgrow[x:x+1]):
					truegrid_check=False
				if len(possibles_c)>0 and (potential_row[x:x+1] not in possibles_c[x][r]):
					truegrid_check=False
			if truegrid_check:
				potential_rows.append(potential_row)
			else:
				slremove.append(potential_space)
		test=0
		for x in slremove:
			spacelist[r].remove(x)
		newtrue=''
		for x in range(num_cols):
			newtrue=newtrue+potential_rows[0][x:x+1]
		for pr in potential_rows:
			for x in range(num_cols):
				if newtrue[x:x+1]!=pr[x:x+1]:newtrue=newtrue[0:x]+'.'+newtrue[x+1:]
		if newtrue!='':
			truegrid[r]=newtrue	
	return [truegrid,spacelist]

def checkinputs(flatrows,flatcols):
	colors=[]
	sumcolors=[]
	checksumcolors=[]
	for cn in flatcols:
		if cn!='0':
			lc=len(cn)
			print(cn)
			i=int(cn[0:lc-1])
			color=cn[lc-1]
			if not(color in colors):
				colors.append(color)
				sumcolors.append(0)
				checksumcolors.append(0)
			intcolor=colors.index(color)
			sumcolors[intcolor]=sumcolors[intcolor]+i
	for r in flatrows:
		if r!='0':
			lr=len(r)
			i=int(r[0:lr-1])
			color=r[lr-1]
			if not(color in colors):
				print("input error:  rows and cols do not match - total colors")
				print(r)
				print(color)
				quit()
			intcolor=colors.index(color)
			checksumcolors[intcolor]=checksumcolors[intcolor]+i
	if len(sumcolors)!=len(checksumcolors):
		##print(str(sc))
		print(len(sumcolors))
		print(colors)
		print(sumcolors)
		print(checksumcolors)
		print("input error:  rows and cols do not match -- total colors")
		quit()
	for sc in range(len(sumcolors)):
		if sumcolors[sc]!=checksumcolors[sc]:
			print("input error:  color totals do not match")
			print(str(sc))
			print(len(sumcolors))
			print(colors)
			print(sumcolors)
			print(checksumcolors)
			print(colors[sc]+" cols "+str(sumcolors[sc])+" vs. rows "+str(checksumcolors[sc]))
			quit()
	return colors

def show_progress(truegrid,last_dot_count):
	solved=True
	topline=' '
	for cn in range(len(truegrid[0])):
		display_cn=str((cn+1)%10)
		topline=topline+display_cn
	print(topline)
	dot_count=0
	for r in range(len(truegrid)):
		display_r=str((r+1)%10)
		print(display_r+truegrid[r]+display_r)
		if truegrid[r].count('.')>0:solved=False
		dot_count+=truegrid[r].count('.')
	progress=dot_count-last_dot_count
	last_dot_count=dot_count
	print(topline)	
	print(str(progress))
	return [solved,last_dot_count]

def careful_rowcheck(truegrid,spacelist,rows,possibles_c=[],colors=[],toobig=25000):
	num_rows=len(rows)
	num_cols=len(truegrid[0])
	for r in range(num_rows):
		print(r)
		row=rows[r]
		blocks=len(row)
		tgrow=truegrid[r]
		## build potential rows
		potential_rows=[]
		slremove=[]
		for potential_space in spacelist[r]:
			if len(spacelist[r])<toobig:
				potential_row=''
				last_color='.'
				for b in range(blocks):
					for x in range(potential_space[b]):
						potential_row=potential_row+" "
					ic=row[b]
					lic=len(ic)
					i=int(ic[0:lic-1])
					c=ic[lic-1:]
					if c==last_color:
						potential_row=potential_row+" "
					for x in range(i):
						potential_row=potential_row+c
					last_color=c
				trailing_spaces=num_cols-len(potential_row)
				for x in range(trailing_spaces):
					potential_row=potential_row+" "
				## potential_row complete.  Check against truegrid.
				truegrid_check=True
				for x in range(len(potential_row)):
					if (tgrow[x:x+1]!='.') and (potential_row[x:x+1]!=tgrow[x:x+1]):
						truegrid_check=False
					if len(possibles_c)>0 and (potential_row[x:x+1] not in possibles_c[x][r]):
						truegrid_check=False
				if truegrid_check:
					potential_rows.append(potential_row)
				else:
					slremove.append(potential_space)
		for x in slremove:
			spacelist[r].remove(x)
		## potential rows are built			
		## find features common to all potential rows
		if len(spacelist[r])<toobig:
			newtrue=''
			for x in range(num_cols):
				newtrue=newtrue+potential_rows[0][x:x+1]
			for pr in potential_rows:
				for x in range(num_cols):
					if newtrue[x:x+1]!=pr[x:x+1]:newtrue=newtrue[0:x]+'.'+newtrue[x+1:]
			if newtrue!='':
				truegrid[r]=newtrue	
	return [truegrid,spacelist]

	
def choose(n,r):
	choose=1
	if n>r:
		choose=math.factorial(n)/(math.factorial(n-r)*math.factorial(r))
	return choose
	
nonogram_solve()

