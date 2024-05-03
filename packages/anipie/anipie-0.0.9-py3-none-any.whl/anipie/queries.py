ANIME_API_URL = "https://graphql.anilist.co"


ANIME_QUERY = """
query ($search: String! $type: MediaType!) { 
            Media (search: $search type: $type) { 
                id
                title {
                    romaji
                    english
                }
                status
                description
                averageScore
                startDate {
                    year
                    month
                    day
                }
                endDate {
                    year
                    month
                    day
                }
                coverImage {
                    large  
                }
                genres
                siteUrl
                episodes
                season
                format
            }
        }
"""

MANGA_QUERY = """
query ($search: String! $type: MediaType!) { 
    Media (search: $search type: $type) { 
        id
        title {
            romaji
            english
        }
        status
        description
        averageScore
        startDate {
            year
            month
            day
        }
        endDate {
            year
            month
            day
        }
        coverImage {
            large  
        }
        genres
        siteUrl
        chapters
        volumes
        format
    }
}
"""
