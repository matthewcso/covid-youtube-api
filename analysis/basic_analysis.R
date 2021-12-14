library(dplyr)
library(readr)
library(anytime)
library(ggplot2)
library(kable)

ls <- list.files('../updated_yt_data')
week_filename <- ls[1]
week_data <- readr::read_csv(paste('../updated_yt_data', week_filename, sep='/'))

for (week_filename in ls[1:length(ls)]){
     week_data <- rbind(week_data, readr::read_csv(paste('../updated_yt_data', week_filename, sep='/')))
}

# ----------------------------------------------------------------------------------------------------- 
day_substring <- function(day){
     return(substr(day, 1, nchar('2019-12-29')))
}

mutated <- week_data %>%
    mutate(codingWeekStartDay = anydate(as.vector(sapply(codingWeek, day_substring)))) %>%
    filter(codingWeekStartDay >= anydate('2019-12-29')) %>%
    filter(duration != 0) %>%
    filter(duration <= 7200)

# -----------------------------------------------------------------------------------------------------

most_popular <- mutated %>%
    top_n(10, viewCount) %>%
    select(c('title', 'publishedAt', 'viewCount', 'videoURL')) %>%
    arrange(desc(viewCount))

viewCount_df <- mutated %>%
    group_by(codingWeekStartDay) %>%
    top_n(20, viewCount) %>%
    summarize(sum_viewCount = sum(viewCount)/1000000, n=n())

#ggplot(viewCount_df) +
#    aes(x=codingWeekStartDay, y=n) +
#    geom_line()

# -----------------------------------------------------------------------------------------------------

plot <- ggplot(viewCount_df) +
    aes(x=codingWeekStartDay, y=sum_viewCount) +
    geom_line() +
    labs(x='Week of', y='Total week view count (millions)')  +
    theme(axis.text.x=element_text(angle=90)) +
    scale_x_date(date_breaks='1 month', date_labels = '%b/%y')

readr::write_csv(mutated, 'updated_all_data.csv')
print(plot)

print(most_popular)
ggsave('week_view_count.png', width=10, height=7)

