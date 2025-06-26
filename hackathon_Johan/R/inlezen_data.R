library(tidyverse)
library(glue)
library(readxl)
library(twn)
library(vegan)
# library(openxlsx)
# library(sf)
# library(leaflet)

theme_set(HHSKwkl::hhskthema())

data <- read_excel("data/Ecologie_tot_2024.xlsx") 
meetpunten <- read_excel("data/Macrofyten_Hackathon_update25_06.xlsx", sheet = "Meetpunt_informatie") %>% 
  rename_all(str_to_lower) %>% 
  rename(mp = meetobject, mpomsch = naam)
planten_info <- read_excel("data/planten_info.xlsx") %>% select(naam, aquatisch, bedekkingslaag)

brondata <- 
  data %>%   
  select(mp = MeetObject, 
         datum = MetingDatumTijd, 
         naam = Parameter, 
         ) %>% 
  mutate(jaar = year(datum),
         maand = month(datum)) %>% 
  distinct() %>% 
  left_join(planten_info) %>% 
  left_join(meetpunten, by = join_by(mp)) %>% 
  mutate(naam = increase_taxonlevel(naam, "Species")) %>% 
  distinct() %>% 
  filter(twn_taxonlevel(naam) <= "Genus")


  
  
  

  
