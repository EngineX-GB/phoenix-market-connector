class Preview:

    def __init__(self, user_id, title, details, start_date, end_date, is_active, business_key):
        self.user_id = user_id
        self.title = title
        self.details = details
        self.start_date = start_date
        self.end_date = end_date
        self.is_active = is_active
        self.business_key = business_key

    def get_user_id(self):
        return self.user_id

    def get_title(self):
        return self.title

    def get_details(self):
        return self.details

    def get_start_date(self):
        return self.start_date

    def get_end_date(self):
        return self.end_date

    def get_business_key(self):
        return self.business_key

    def generate_record(self):
        return self.user_id + "|" + self.title + "|" + self.details + "|" + self.start_date + "|" + self.end_date + "|" + self.business_key


class PreviewCollapsedLine:

    def __init__(self, user_id, country, region, county, town, postcode, details, start_date, end_date, business_key):
        self.user_id = user_id
        self.country = country
        self.region = region
        self.county = county
        self.town = town
        self.postcode = postcode
        self.details = details
        self.start_date = start_date
        self.end_date = end_date
        self.business_key = business_key

    def generate_record(self):
        return self.user_id + "|" + self.country + "|" + self.region + "|" + self.county + "|" + self.town + "|" + self.postcode + "|" + self.details + "|" + self.start_date + "|" + self.end_date + "|" + self.business_key

    def get_user_id(self):
        return self.user_id

    def get_country(self):
        return self.country

    def get_region(self):
        return self.region

    def get_county(self):
        return self.county

    def get_town(self):
        return self.town

    def get_postcode(self):
        return self.postcode

    def get_details(self):
        return self.details

    def get_start_date(self):
        return self.start_date

    def get_end_date(self):
        return self.end_date

    def get_business_key(self):
        return self.business_key


class PreviewExpandedLine:

    def __init__(self, user_id, country, region, county, town, postcode, details, availability_date, business_key):
        self.user_id = user_id
        self.country = country
        self.region = region
        self.county = county
        self.town = town
        self.postcode = postcode
        self.details = details
        self.availability_date = availability_date
        self.business_key = business_key

    def generate_record(self):
        return self.user_id + "|" + self.country + "|" + self.region + "|" + self.county + "|" + self.town + "|" + self.postcode + "|" + self.details + "|" + self.availability_date + "|" + self.business_key

    def get_user_id(self):
        return self.user_id

    def get_country(self):
        return self.country

    def get_region(self):
        return self.region

    def get_county(self):
        return self.county

    def get_town(self):
        return self.town

    def get_postcode(self):
        return self.postcode

    def get_details(self):
        return self.details

    def get_availability_date(self):
        return self.availability_date

    def get_business_key(self):
        return self.business_key


class PreviewDataHolder:

    def __init__(self, preview_headers, preview_collapsed_lines, preview_expanded_lines):
        self.preview_headers = preview_headers
        self.preview_collapsed_lines = preview_collapsed_lines
        self.preview_expanded_lines = preview_expanded_lines

    def get_preview_header(self):
        return self.preview_headers

    def get_preview_collapsed_lines(self):
        return self.preview_collapsed_lines

    def get_preview_expanded_lines(self):
        return self.preview_expanded_lines
