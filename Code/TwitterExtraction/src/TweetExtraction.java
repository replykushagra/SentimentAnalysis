import java.awt.Color;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;
import java.util.ArrayList;
import java.util.List;
import java.util.Random;

import au.com.bytecode.opencsv.CSVReader;
import au.com.bytecode.opencsv.CSVWriter;
import twitter4j.Query;
import twitter4j.QueryResult;
import twitter4j.Status;
import twitter4j.Twitter;
import twitter4j.TwitterFactory;
import twitter4j.conf.ConfigurationBuilder;




public class TweetExtraction {
	 private final static String CONSUMER_KEY = "AwQMUbv0Xv3HySho6M3g";
	 private final static String CONSUMER_KEY_SECRET = "zRTGWtR4LR65JuCIOE5qaugsQYtoZflLRXB9wDaY";
	 private final static String OAUTH_ACCESS_TOKEN="2187929912-v6noxazqZkz5n76bD7BD7ZdMKUVgGT5ueAO9WQx";
	 private final static String OAUTH_TOKEN_SECRET="oXbJi65jnCi8F5X3rlG0aggp90f6luFHP9qR9bxvIbkkV";
	 
	 
	 
	 
	public static void writeTweets() throws IOException 
	{
		CSVReader csvReader=new CSVReader(new FileReader("F:\\TwitterSentimentAnalysis\\the_dark_night_rises.csv"));
		List<String[]> olderTweets=csvReader.readAll();
        csvReader.close();
		CSVWriter csvWriter=new CSVWriter(new FileWriter("F:\\TwitterSentimentAnalysis\\Tweets_night_at_the_museum.csv"));
		ConfigurationBuilder cb = new ConfigurationBuilder();
        cb.setDebugEnabled(true)
          .setOAuthConsumerKey(CONSUMER_KEY)
          .setOAuthConsumerSecret(CONSUMER_KEY_SECRET)
          .setOAuthAccessToken(OAUTH_ACCESS_TOKEN)
          .setOAuthAccessTokenSecret(OAUTH_TOKEN_SECRET);
        List<String[]> newTweetsList=new ArrayList<String[]>();
        
        try 
        {					 
	        TwitterFactory tFactory=new TwitterFactory(cb.build());
			Twitter twitter = tFactory.getInstance();
			Query query = new Query("night at the museum"); 
			query.setLang("en");
			QueryResult qr; 
			do
			{ 
				try {
					qr = twitter.search(query); 
				} catch (Exception e) {
					break;
				}
				
				List<Status> qrTweets = qr.getTweets(); 
				if(qrTweets.size() == 0) 
					System.out.println("0 tweets"); 
				for(Status t : qrTweets) 
				{ 
					System.out.println(t.getId() + " - " + t.getCreatedAt() + ": " + t.getText()); //dumpCsv("Homefront.csv",t.getText()); counter++; } //System.out.println();
					String[] strline=new String[3];
					strline[0]=t.getId()+"";
					strline[1]=t.getCreatedAt().toString();
					strline[2]=t.getText();
					newTweetsList.add(strline);
					Query next=qr.nextQuery(); 
					while((next == null) && (qr.getRateLimitStatus().getRemaining()) > 0)
					{ 
						
						System.out.println(qr.getRateLimitStatus().getSecondsUntilReset());
						break;
					} 
					query = next; 													
				} 
			
			}
			while (qr.getRateLimitStatus().getRemaining() > 0);
			
			olderTweets.addAll(newTweetsList);
			csvWriter.writeAll(olderTweets);
			csvWriter.close();
			
			
        }
		catch (Exception e) {
			System.out.println(e.getMessage());
			e.printStackTrace();
		}
	}
	public static void main(String[] args) throws IOException
	{	
		TweetExtraction tweetExtraction=new TweetExtraction();
		tweetExtraction.writeTweets();
	}
}
