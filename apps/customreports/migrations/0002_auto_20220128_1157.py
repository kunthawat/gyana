# Generated by Django 3.2.11 on 2022-01-28 11:57

import apps.base.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("customreports", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="facebookadscustomreport",
            name="fields",
            field=apps.base.fields.ChoiceArrayField(
                base_field=models.CharField(
                    choices=[
                        ("account_id", "account_id"),
                        ("account_name", "account_name"),
                        ("action_values", "action_values"),
                        ("actions", "actions"),
                        ("ad_id", "ad_id"),
                        ("ad_name", "ad_name"),
                        ("adset_id", "adset_id"),
                        ("adset_name", "adset_name"),
                        ("buying_type", "buying_type"),
                        ("campaign_id", "campaign_id"),
                        ("campaign_name", "campaign_name"),
                        ("canvas_avg_view_percent", "canvas_avg_view_percent"),
                        ("canvas_avg_view_time", "canvas_avg_view_time"),
                        ("clicks", "clicks"),
                        ("cost_per_10_sec_video_view", "cost_per_10_sec_video_view"),
                        ("cost_per_action_type", "cost_per_action_type"),
                        ("cost_per_inline_link_click", "cost_per_inline_link_click"),
                        (
                            "cost_per_inline_post_engagement",
                            "cost_per_inline_post_engagement",
                        ),
                        ("cost_per_outbound_click", "cost_per_outbound_click"),
                        ("cost_per_unique_action_type", "cost_per_unique_action_type"),
                        ("cost_per_unique_click", "cost_per_unique_click"),
                        (
                            "cost_per_unique_inline_link_click",
                            "cost_per_unique_inline_link_click",
                        ),
                        (
                            "cost_per_unique_outbound_click",
                            "cost_per_unique_outbound_click",
                        ),
                        ("cpc", "cpc"),
                        ("cpm", "cpm"),
                        ("cpp", "cpp"),
                        ("ctr", "ctr"),
                        ("frequency", "frequency"),
                        ("gender_targeting", "gender_targeting"),
                        ("impressions", "impressions"),
                        ("inline_link_click_ctr", "inline_link_click_ctr"),
                        ("inline_link_clicks", "inline_link_clicks"),
                        ("inline_post_engagement", "inline_post_engagement"),
                        ("labels", "labels"),
                        ("location", "location"),
                        ("mobile_app_purchase_roas", "mobile_app_purchase_roas"),
                        ("objective", "objective"),
                        ("outbound_clicks", "outbound_clicks"),
                        ("outbound_clicks_ctr", "outbound_clicks_ctr"),
                        ("reach", "reach"),
                        ("relevance_score", "relevance_score"),
                        ("social_spend", "social_spend"),
                        ("spend", "spend"),
                        ("unique_actions", "unique_actions"),
                        ("unique_clicks", "unique_clicks"),
                        ("unique_ctr", "unique_ctr"),
                        (
                            "unique_inline_link_click_ctr",
                            "unique_inline_link_click_ctr",
                        ),
                        ("unique_inline_link_clicks", "unique_inline_link_clicks"),
                        ("unique_link_clicks_ctr", "unique_link_clicks_ctr"),
                        ("unique_outbound_clicks", "unique_outbound_clicks"),
                        ("unique_outbound_clicks_ctr", "unique_outbound_clicks_ctr"),
                        (
                            "video_10_sec_watched_actions",
                            "video_10_sec_watched_actions",
                        ),
                        (
                            "video_30_sec_watched_actions",
                            "video_30_sec_watched_actions",
                        ),
                        (
                            "video_avg_percent_watched_actions",
                            "video_avg_percent_watched_actions",
                        ),
                        (
                            "video_avg_time_watched_actions",
                            "video_avg_time_watched_actions",
                        ),
                        ("video_p100_watched_actions", "video_p100_watched_actions"),
                        ("video_p25_watched_actions", "video_p25_watched_actions"),
                        ("video_p50_watched_actions", "video_p50_watched_actions"),
                        ("video_p75_watched_actions", "video_p75_watched_actions"),
                        ("video_p95_watched_actions", "video_p95_watched_actions"),
                        ("website_ctr", "website_ctr"),
                        ("website_purchase_roas", "website_purchase_roas"),
                        ("purchase_roas", "purchase_roas"),
                        ("conversion_rate_ranking", "conversion_rate_ranking"),
                        ("conversion_values", "conversion_values"),
                        ("conversions", "conversions"),
                        ("cost_per_conversion", "cost_per_conversion"),
                        (
                            "cost_per_estimated_ad_recallers",
                            "cost_per_estimated_ad_recallers",
                        ),
                        ("cost_per_thruplay", "cost_per_thruplay"),
                        ("engagement_rate_ranking", "engagement_rate_ranking"),
                        ("estimated_ad_recall_rate", "estimated_ad_recall_rate"),
                        ("estimated_ad_recallers", "estimated_ad_recallers"),
                        ("full_view_impressions", "full_view_impressions"),
                        ("full_view_reach", "full_view_reach"),
                        (
                            "instant_experience_clicks_to_open",
                            "instant_experience_clicks_to_open",
                        ),
                        (
                            "instant_experience_clicks_to_start",
                            "instant_experience_clicks_to_start",
                        ),
                        (
                            "instant_experience_outbound_clicks",
                            "instant_experience_outbound_clicks",
                        ),
                        ("quality_ranking", "quality_ranking"),
                        ("video_play_actions", "video_play_actions"),
                        ("video_play_curve_actions", "video_play_curve_actions"),
                        (
                            "video_thruplay_watched_actions",
                            "video_thruplay_watched_actions",
                        ),
                    ],
                    max_length=64,
                ),
                size=None,
            ),
        ),
        migrations.AlterField(
            model_name="facebookadscustomreport",
            name="table_name",
            field=models.CharField(default="Untitled custom report", max_length=1024),
        ),
    ]
