# This file was generated, do not modify it. # hide
A = reshape(collect(1:9), 3,3);
println(isa(A, Array{Number, 2}))
isa(A, Array{<:Number, 2})