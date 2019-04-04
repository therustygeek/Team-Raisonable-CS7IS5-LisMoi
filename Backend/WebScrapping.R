install.packages("rvest")
library("rvest")
mainURLS <- c("https://www.goodreads.com/shelf/show/mystery","https://www.goodreads.com/shelf/show/romance","https://www.goodreads.com/shelf/show/humor","https://www.goodreads.com/shelf/show/science-fiction","https://www.goodreads.com/shelf/show/adventure")
rm(dataFrameFinal)

for(j in 1:5){
  
  mysteryPage <- read_html(mainURLS[j])

URLS <- mysteryPage %>% html_nodes(".bookTitle") %>% html_attr('href')
class(URLS)
URLS_full <- c()
for(i in 1:length(URLS)){
  appended <- paste0("https://www.goodreads.com",URLS[i])
  URLS_full <- append(URLS_full,appended)  
}

genre <-c( "Mystery","Romance","Humor","Science Fiction","Adventure")

genreVector <- c()
booknameVector <- c()
authorNameVector <- c()
summaryVector <- c()
bookcoverURLVector <- c()



for(i in 1:length(URLS_full)){
pageToScan <- read_html(URLS_full[i])  
urlGoodread[i] <- URLS_full[i]
bookName <-  pageToScan %>% html_nodes("#bookTitle") %>% html_text()
bookname <- gsub("\n","",bookName)
bookname <- trimws(bookname,"l")
booknameVector[i] <- bookname


authorName <-  pageToScan %>% html_nodes("#bookAuthors") %>% html_text()
authorName <- gsub("\n","",authorName)
authorName <- trimws(authorName,"l")
authorNameVector[i] <- substring(authorName, 3)

summary <-  pageToScan %>% html_nodes("#description") %>% html_text()
summary <-gsub("\n","",summary)
summary <- trimws(summary,"l")
summaryVector[i] <- gsub("  ...more      ","",summary)

bookcoverURL <- pageToScan %>% html_nodes("#coverImage") %>% html_attr('src')
bookcoverURLVector[i] <-bookcoverURL

genreVector[i] <- genre[j]

}
if(j ==1){
dataFrameFinal <-data.frame(genreVector,booknameVector,authorNameVector,summaryVector,bookcoverURLVector,urlGoodread)
}else{
  dataFrameTemp <-data.frame(genreVector,booknameVector,authorNameVector,summaryVector,bookcoverURLVector,urlGoodread)
  dataFrameFinal <- rbind(dataFrameFinal,dataFrameTemp)
  
}
print(genre[j])}

write.csv(x =dataFrameFinal,file = "bookrecommendationdata.CSV" )
