SRC=$(basename $(wildcard *.ipynb))
OUT=$(addsuffix .out,$(SRC))
HTML=$(addprefix html/,$(addsuffix .html,$(SRC)))


all: run tohtml


run: $(OUT)


tohtml: $(HTML)


%.out: %.ipynb
	jupyter nbconvert --ExecutePreprocessor.timeout=1800 --to notebook --execute $< --output $@
	mv $@.ipynb $@

html/%.html: %.out
	jupyter nbconvert $< --output $@

clean:
	rm -f $(OUT) $(HTML)
