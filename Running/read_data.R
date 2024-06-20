library(tidyverse)
library(reticulate)

# source_python('D:/maps/Running/pickle_reader.py')
# gpx.data <- read_pickle_file('D:/maps/Running/Data/kg_06142024_gpx.pkl')

py_install('pandas')
pd <- import('pandas')
gpx.data <- pd$read_pickle('./Data/gpx.pkl')

data <- gpx.data

rm(pd, gpx.data)
gc()

data %>% distinct(Type)

running <- data %>%
  filter(Type == 'running')
cycling <- data %>%
  filter(Type == 'cycling')

saveRDS(running, file = './Data/kg_running_06142024.RDS')
saveRDS(cycling, file = './Data/kg_cycling_06142024.RDS')
