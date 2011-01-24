
SPECIES = CO3s1 CO3s2 CO3s4 CO3t1 CO3t2 \
          cyclopropene12diyl cyclopropynylidyne
LIBRARY = Library.txt
DICTIONARY = Dictionary.txt
DATADIR = data

CANTHERMOUT=$(patsubst %,$(DATADIR)/%.out,$(SPECIES))

data: $(LIBRARY) $(DICTIONARY)

$(LIBRARY): $(CANTHERMOUT) combine.py
	python combine.py $(CANTHERMOUT) | tee $(LIBRARY)

$(DICTIONARY): $(DATADIR)/*.chemgraph
	cat $(DATADIR)/*.chemgraph > $(DICTIONARY)

cantherm: $(CANTHERMOUT)

%.out : %.dat
	python ../CanTherm/source/CanTherm.py $< | tee $@
	mv cantherm.out $*.log

clean:
	rm -f $(CANTHERMOUT) $(LIBRARY) $(DICTIONARY)