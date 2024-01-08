# Steam Games Dataset

## `steam_games.json`

This dataset provides comprehensive information about games, covering details such as title, developer, prices, technical specifications, and tags.

- **publisher**: The company responsible for publishing the content.
- **genres**: The genre(s) of the game, represented as a list of one or more genres per record.
- **app_name**: The name of the game.
- **title**: The title of the game.
- **url**: The URL of the game.
- **release_date**: The release date of the game in the format YYYY-MM-DD.
- **tags**: Tags associated with the content, presented as a list of one or more tags per record.
- **discount_price**: The discounted price of the product.
- **reviews_url**: The URL where the reviews for the game can be found.
- **specs**: Specifications for each item, presented as a list of one or more strings with the specifications.
- **price**: The price of the item.
- **early_access**: Indicates whether the item has early access with a True/False value.
- **id**: The unique identifier for the content.
- **developer**: The developer of the content.
- **metascore**: Metacritic score.

# User Reviews Dataset

## `user_reviews.json`

This dataset contains user reviews for games, along with additional data such as recommendations, funny emoticons, and statistics on the helpfulness of reviews.

- **user_id**: Unique identifier for the user.
- **user_url**: URL of the user's profile on Steam Community.
- **reviews**: A list of dictionaries containing user reviews. Each dictionary includes:
  - **funny**: Indicates if someone used a funny emoticon in the review.
  - **posted**: The posting date of the review in the format "Posted April 21, 2011."
  - **last_edited**: The date of the last edit.
  - **item_id**: The unique identifier of the item (game) being reviewed.
  - **helpful**: Statistics where other users indicate if the information was helpful.
  - **recommend**: A boolean indicating whether the user recommends the game.
  - **review**: A string sentence with comments about the game.

# User Items Dataset

## `user_items.json`

This dataset provides information on the games played by users, including accumulated playtime for each game.

- **steam_id**: Unique number for the platform.
- **user_url**: URL of the user's profile.
- **items**: A list of one or more dictionaries containing information about the items (games) each user consumes. Each dictionary includes:
  - **item_id**: The identifier of the item (game).
  - **item_name**: The name of the consumed content (game).
  - **playtime_forever**: The accumulated time a user has played a game.
  - **playtime_2weeks**: The accumulated time a user has played a game in the last two weeks.
