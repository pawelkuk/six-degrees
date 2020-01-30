library(tidyverse)

setwd(dirname(rstudioapi::getActiveDocumentContext()$path))
df <- read.csv("scraper_data.csv")

df %>% 
  mutate(
    scraper = str_trim(scraper)
  ) %>% 
  ggplot(
    aes(scraper, time)
  ) +
  stat_summary(
    geom = "bar",
    fun.y = mean, 
    position = "dodge"
  ) +
  stat_summary(
    geom = "errorbar",
    fun.data = mean_se, 
    position = "dodge"
  ) +
  coord_flip() +
  facet_wrap(~ strony + komp) +
  theme_bw()
