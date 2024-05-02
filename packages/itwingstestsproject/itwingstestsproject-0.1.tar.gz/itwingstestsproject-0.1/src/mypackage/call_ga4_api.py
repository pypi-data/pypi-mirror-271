from google.analytics.data_v1beta import BetaAnalyticsDataClient
from google.analytics.data_v1beta.types import DateRange, Metric, RunReportRequest, Dimension, FilterExpression, Filter, FilterExpressionList
from google.oauth2 import service_account
from utils.raw_data_to_csv import raw_data_to_csv
from configuration.config import *

from google.api_core.exceptions import GoogleAPICallError

def call_ga4_api(url, ga4, ga4_property_id, credentials):
    try:
        if ga4 == "yes":
            credentials = service_account.Credentials.from_service_account_info(credentials)
            client = BetaAnalyticsDataClient(credentials=credentials)

            request = RunReportRequest(
                property=f"properties/{ga4_property_id}",
                dimensions=[Dimension(name="sessionMedium")],
                metrics=[
                    Metric(name="totalUsers"),
                    Metric(name="sessions"),
                    Metric(name="bounceRate"),
                    Metric(name="averageSessionDuration"),
                    Metric(name="engagementRate")
                ],
                date_ranges=[DateRange(start_date=start_date_ga4, end_date=end_date_ga4)],
            )
            response = client.run_report(request)

            # Initialize counters
            total_sessions = 0
            organic_sessions = 0
            total_users = 0
            bounce_rate_sum = 0
            avg_session_duration_sum = 0
            engagement_rate_sum = 0

            # Process response to calculate metrics
            for row in response.rows:
                sessions = int(row.metric_values[1].value)
                total_sessions += sessions
                total_users += int(row.metric_values[0].value)
                bounce_rate_sum += float(row.metric_values[2].value) * sessions
                avg_session_duration_sum += float(row.metric_values[3].value) * sessions
                engagement_rate_sum += float(row.metric_values[4].value) * sessions

                if row.dimension_values[0].value.lower() == "organic":
                    organic_sessions += sessions

            # Calculate metrics
            percentage_organic_traffic = (organic_sessions / total_sessions * 100) if total_sessions > 0 else 0
            average_bounce_rate = (bounce_rate_sum / total_sessions) if total_sessions > 0 else 0
            average_session_duration = (avg_session_duration_sum / total_sessions) if total_sessions > 0 else 0
            average_engagement_rate = (engagement_rate_sum / total_sessions) if total_sessions > 0 else 0

            # Create the single result row
            row_data = {
                "url": url,
                "Organic Traffic": organic_sessions,
                "Percentage Organic Traffic": f"{percentage_organic_traffic:.2f}%",
                "Total Users": total_users,
                "Average Bounce Rate": f"{average_bounce_rate:.2%}",
                "Average Session Duration": f"{average_session_duration:.2f}",
                "Average Engagement Rate": f"{average_engagement_rate:.2%}",
                "Phase 3": passed_or_failed(percentage_organic_traffic, average_bounce_rate)
            }
            rows = [row_data]

            # Using the adapted function to write/append to CSV
            raw_data_to_csv("ga4", rows, append=True)
        else:
            row_data = {
                "url": url,
                "Organic Traffic": "-",
                "Percentage Organic Traffic": "-",
                "Total Users": "-",
                "Average Bounce Rate": "-",
                "Average Session Duration": "-",
                "Average Engagement Rate": "-",
                "Phase 3": "no access"
            }
            rows = [row_data]
            raw_data_to_csv("ga4", rows, append=True)
    except GoogleAPICallError as e:
        print(f"Error: {e}")
        # Save "no access" to CSV in case of an error
        row_data = {
            "url": url,
            "Organic Traffic": "-",
            "Percentage Organic Traffic": "-",
            "Total Users": "-",
            "Average Bounce Rate": "-",
            "Average Session Duration": "-",
            "Average Engagement Rate": "-",
            "Phase 3": "no access"
        }
        rows = [row_data]
        raw_data_to_csv("ga4", rows, append=True)

# Function to determine passed or failed based on the given thresholds
def passed_or_failed(percentage_organic_traffic, average_bounce_rate):
    # Check Impressions
    if percentage_organic_traffic > 65:
        return 'failed'
    # Check Clicks
    elif average_bounce_rate > 55:
        return 'failed'
    # Check Average Position
    # elif check_average_position > thresholds['Average Position']['Green']:
    #     return 'failed'
    else:
        return 'passed'
