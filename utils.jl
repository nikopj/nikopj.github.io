using Dates
import Franklin

function hfun_bar(vname)
	val = Meta.parse(vname[1])
	return round(sqrt(val), digits=2)
end

function hfun_m1fill(vname)
	var = vname[1]
	return pagevar("index", var)
end

function hfun_recentposts(dir)
	dir = dir[1]
	list = readdir(dir)
	filter!(f -> endswith(f, ".md"), list)
	#dates = [stat(joinpath("blog", f)).mtime for f in list]
	dates = [Dates.date2epochdays(pagevar(splitext(joinpath(dir, f))[1], :date)) for f in list]
	perm = sortperm(dates, rev=true)
	idxs = perm[1:length(perm)]
	io = IOBuffer()
	#write(io, "<ul>")
	for (k, i) in enumerate(idxs)
		fi = "/" * dir * "/" * splitext(list[i])[1] * "/"
		sfi = strip(fi,'/')
		d = pagevar(sfi, :date) 
		ds = Dates.format(d, "d U Y")
		du = Dates.date2epochdays(d)
		t = pagevar(sfi, :title)
		tags = pagevar(sfi, :tags)
		if "notes" ∈ tags
			continue
		end
		#write(io, """<li><a href="$fi">$t</a> $d</li>\n""")
		mds = Franklin.md2html("- **[$t]($fi)**")
		write(io, mds)
		#write(io, "$du \n")
		descr = pagevar(sfi, :descr)
		fds = Franklin.fd2html("$descr ..."; internal=true)
		write(io, fds)
	end
	#write(io, "</ul>")
	return String(take!(io))
end

function lx_baz(com, _)
	# keep this first line
	brace_content = Franklin.content(com.braces[1]) # input string
	# do whatever you want here
	return uppercase(brace_content)
end
