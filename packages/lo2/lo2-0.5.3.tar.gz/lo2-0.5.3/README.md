## lo2 (lo2-lang) - Log Oracle, an Oracle test language for log description and analysis.

lo2 is a domain-specific programming language (DSL) designed to describe log behavior, originating from Oracle testing. By describing log behavior, it analyzes logs to discover actions that violate expected (Oracle) rules.

1. Install
```sh
python -m pip install lo2
```

2. Quickly Example

```sh
python3 -m lo2 -s demo/demo.lo2  -l demo/demo_lo2.log -c
```

The `-s` parameter specifies a lo2 source code file, which describes the expected behavior of the log file. The `-l` parameter specifies `demo_lo2.log`, a log file being analyzed. This command will output whether `demo_lo2.log` has experienced unexpected abnormal behavior **(Contrary to Oracle)**

3. Tutorial

Regarding the syntax tutorial for the Lo2 language, we will organize and supplement it later.

4. Editor highlighting-syntax plugin

The lo2 language has its own syntax highlighting-syntax plugin, which is available in the [vscode](https://marketplace.visualstudio.com/items?itemName=alextee.lo2-highlighter), or seach for `lo2-highlighter` in the extension market.
