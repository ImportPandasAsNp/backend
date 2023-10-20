def ageRatingList(rating):
    mappings = {
        'A': ['18+','R','NR' 'PG-13', '13+', 'TV-14', 'PG', 'TV-MA', '16+', 'G', 'TV-G', 'TV-PG', 'TV-Y7', 'TV-Y7-FV', 'TV-Y', '7+', 'NOT_RATE', '74 min', '84 min', '66 min', 'UR', 'nan'],
        'U/A': ['PG-13', '13+', 'TV-14', 'PG', 'TV-MA', '16+', 'G', 'TV-G', 'TV-PG', 'TV-Y7', 'TV-Y7-FV', 'TV-Y', '7+', 'NOT_RATE', '74 min', '84 min', '66 min', 'UR', 'nan'],
        'U': ['G', 'TV-G', 'TV-PG', 'TV-Y7', 'TV-Y7-FV', 'TV-Y', '7+', 'NOT_RATE', '74 min', '84 min', '66 min', 'UR', 'nan']
    }

    return mappings[rating]