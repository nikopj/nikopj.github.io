## Reminders on how to use Franklin.jl

1. open julia
2. activate environment: `activate .`
3. serve website while developing: `using Franklin; serve()`
4. commit and push to deploy

Global variables are defined in the `config.md` page and can be accessed via,
```plaintext
{{var}}
```

Local variables (defined in other pages) can be accessed by specifying their 
location of definition, ex.

```plaintext
{{fill title blog/dcdl.md}}
```

## TODO:
- Social badges in footnote
- comments
