class ServiceReportFeed:

    def __init__(self, candidate_description, candidate_description_score, client_nickname, comments, comments_score,
                 create_date, exclude_affiliate, fee, id, location, meet_date, meet_duration, nickname, oncall,
                 personality, personality_score, rating_total, recommend, rejected, report_rating, schema_id,
                 schema_last_updated, score, services, services_score, user_id, venue_description, venue_score, vfm,
                 visit_again):
        self.candidate_description = candidate_description
        self.candidate_description_score = candidate_description_score
        self.client_nickname = client_nickname
        self.comments = comments
        self.comments_score = comments_score
        self.create_date = create_date
        self.exclude_affiliate = exclude_affiliate
        self.fee = fee
        self.id = id
        self.location = location
        self.meet_date = meet_date
        self.meet_duration = meet_duration
        self.nickname = nickname
        self.oncall = oncall
        self.personality = personality
        self.personality_score = personality_score
        self.rating_total = rating_total
        self.recommend = recommend
        self.rejected = rejected
        self.report_rating = report_rating
        self.schema_id = schema_id
        self.schema_last_updated = schema_last_updated
        self.score = score
        self.services = services
        self.services_score = services_score
        self.user_id = user_id
        self.venue_description = venue_description
        self.venue_score = venue_score
        self.vfm = vfm
        self.visit_again = visit_again
        self.DELIMITER = "|"


    def parse_value(self, value):
        if value is None:
            return "None"
        return value

    def parse_and_clean_value(self, value):
        if value is None:
            return "None"
        return value.replace("\r\n", "\\r\\n").replace("\n", "\\n").replace("\r", "\\r")


    def generate_record(self):
        return "".join([self.parse_value(self.id) + self.DELIMITER,
                        self.parse_value(self.user_id) + self.DELIMITER,
                        self.parse_and_clean_value(self.nickname) + self.DELIMITER,
                        self.parse_and_clean_value(self.candidate_description) + self.DELIMITER,
                        self.parse_value(self.candidate_description_score) + self.DELIMITER,
                        self.parse_and_clean_value(self.client_nickname) + self.DELIMITER,
                        self.parse_and_clean_value(self.comments) + self.DELIMITER,
                        self.parse_value(self.comments_score) + self.DELIMITER,
                        self.parse_value(self.create_date) + self.DELIMITER,
                        self.parse_value(self.exclude_affiliate) + self.DELIMITER,
                        self.parse_and_clean_value(self.fee) + self.DELIMITER,
                        self.parse_and_clean_value(self.location) + self.DELIMITER,
                        self.parse_value(self.meet_date) + self.DELIMITER,
                        self.parse_and_clean_value(self.meet_duration) + self.DELIMITER,
                        self.parse_value(self.oncall) + self.DELIMITER,
                        self.parse_and_clean_value(self.personality) + self.DELIMITER,
                        self.parse_value(self.personality_score) + self.DELIMITER,
                        self.parse_value(self.rating_total) + self.DELIMITER,
                        self.parse_value(self.recommend) + self.DELIMITER,
                        self.parse_value(self.rejected) + self.DELIMITER,
                        self.parse_and_clean_value(self.report_rating) + self.DELIMITER,
                        self.parse_value(self.schema_id) + self.DELIMITER,
                        self.parse_value(self.schema_last_updated) + self.DELIMITER,
                        self.parse_value(self.score) + self.DELIMITER,
                        self.parse_and_clean_value(self.services) + self.DELIMITER,
                        self.parse_value(self.services_score) + self.DELIMITER,
                        self.parse_and_clean_value(self.venue_description) + self.DELIMITER,
                        self.parse_value(self.venue_score) + self.DELIMITER,
                        self.parse_and_clean_value(self.vfm) + self.DELIMITER,
                        self.parse_value(self.visit_again)])