from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.conf import settings

from elasticsearch import Elasticsearch

from datetime import datetime, timedelta
import json


TEST_DATA_ENABLED = True  # 테스트 데이터 사용 여부 설정

if TEST_DATA_ENABLED:
    # 테스트 데이터 파일에서 가상 데이터 로드
    def daily_on_off_times_offline(selected_date):
        with open("offline_leds.json", "r") as file:
            data = json.load(file)
    
        daily_on_off_times = []
        
        for item in data:
            date = item["date"]
            start_time = item["start_time"]
            end_time = item["end_time"]
            led = item["led"]
            
            if selected_date and date != str(selected_date):
                continue

            daily_on_off_times.append({
                "date": date,
                "start_time": start_time,
                "end_time": end_time,
                "led": led
            })

        return daily_on_off_times

    def daily_on_off_sum_offline(selected_date):
        with open("offline_leds_sum.json", "r") as file:
            data = json.load(file)
    
        daily_on_off_sum_times = []
        
        for item in data:
            date = item["date"]
            on_time = item["on_time"]
            off_time = item["off_time"]
            
            if selected_date and date != str(selected_date):
                continue
                
            daily_on_off_sum_times.append({
                "date": date,
                "on_time": on_time,
                "off_time": off_time,
            })

        return daily_on_off_sum_times

else:
    # Elasticsearch 연결 정보 가져오기
    ELASTICSEARCH_HOST = settings.ELASTICSEARCH_HOST
    ELASTICSEARCH_PORT = settings.ELASTICSEARCH_PORT
    ELASTICSEARCH_USERNAME = settings.ELASTICSEARCH_USERNAME
    ELASTICSEARCH_PASSWORD = settings.ELASTICSEARCH_PASSWORD
    
    from elasticsearch import Elasticsearch

    es_client = Elasticsearch(
        hosts=[{'host': ELASTICSEARCH_HOST, 'port': ELASTICSEARCH_PORT}],
        http_auth=(ELASTICSEARCH_USERNAME, ELASTICSEARCH_PASSWORD)
    )

    # Elasticsearch 연결 테스트
    if es_client.ping():
        print("Connected to Elasticsearch")
    else:
        print("Failed to connect to Elasticsearch")


def get_onoff_daily_minutes(es_client, selected_date=None):
    query = {
        "query": {
            "bool": {
                "must": [
                    {
                        "exists": {
                            "field": "led_state"
                        }
                    },
                    {
                        "terms": {
                            "led_state.keyword": ["ON", "OFF"]
                        }
                    }
                ]
            }
        },
        "aggs": {
            "daily_agg": {
                "date_histogram": {
                    # "field": "@timestamp",
                    "field": "start_time",  # Use the "start_time" field for date histogram aggregation
                    "calendar_interval": "1d"  # Daily interval
                },
                "aggs": {
                    "on_time": {
                        "filter": {
                            "term": {
                                "led_state.keyword": "ON"
                            }
                        },
                        "aggs": {
                            "total_on_time": {
                                "sum": {
                                    "script": {
                                        "source": "(doc['end_time'].value.toInstant().toEpochMilli() - doc['start_time'].value.toInstant().toEpochMilli()) / (1000 * 60)"
                                    }
                                }
                            }
                        }
                    },
                    "off_time": {
                        "filter": {
                            "term": {
                                "led_state.keyword": "OFF"
                            }
                        },
                        "aggs": {
                            "total_off_time": {
                                "sum": {
                                    "script": {
                                        "source": "(doc['end_time'].value.toInstant().toEpochMilli() - doc['start_time'].value.toInstant().toEpochMilli()) / (1000 * 60)"
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
    }

    if selected_date:
        start_date = datetime.combine(selected_date, datetime.min.time())
        end_date = start_date + timedelta(days=1)

        query["query"]["bool"]["must"].append({
            "range": {
                "start_time": {
                    "gte": start_date,
                    "lt": end_date
                }
            }
        })

    result = es_client.search(index="google_fitness", body=query)
    # Result processing
    daily_results = result["aggregations"]["daily_agg"]["buckets"]
    daily_on_off_times = []

    for daily_time in daily_results:
        # date = daily_time["key_as_string"]
        date = datetime.strptime(daily_time["key_as_string"], "%Y-%m-%dT%H:%M:%S.%fZ").date()
        on_time = int(daily_time["on_time"]["total_on_time"]["value"]) # int 변환하여 소수점 제거
        off_time = int(daily_time["off_time"]["total_off_time"]["value"])

        daily_on_off_times.append({
            "date": date,
            "on_time": on_time,
            "off_time": off_time
        })

    return daily_on_off_times


def get_daily_minutes(es_client, selected_date=None):
    query = {
        "query": {
            "bool": {
                "must": [
                    {
                        "exists": {
                            "field": "led_state"
                        }
                    },
                    {
                        "terms": {
                            "led_state.keyword": ["ON", "OFF"]
                        }
                    }
                ]
            }
        },
        "sort": [
            {
                # "@timestamp": {
                "start_time": {
                    "order": "asc"
                }
            }
        ],
        "size": 100  # 최대 100개의 결과 반환 (기본값은 10개)
    }

    if selected_date:
        start_date = datetime.combine(selected_date, datetime.min.time())
        end_date = start_date + timedelta(days=1)

        query["query"]["bool"]["must"].append({
            "range": {
                "start_time": {
                    "gte": start_date,
                    "lt": end_date
                }
            }
        })

    result = es_client.search(index="google_fitness", body=query)
    daily_results = result["hits"]["hits"]
    daily_on_off_times = []

    for daily_time in daily_results:
        timestamp = daily_time["_source"]["@timestamp"]
        date = datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%S.%fZ").date()

        # start_time = daily_time["_source"]["message"].split("StartTime: ")[1].split(",")[0]
        # end_time = daily_time["_source"]["message"].split("EndTime: ")[1].split(",")[0]
        # led = daily_time["_source"]["message"].split("LED: ")[1]

        start_time = datetime.strptime(daily_time["_source"]["start_time"], "%Y-%m-%dT%H:%M:%S.%fZ").strftime("%Y-%m-%d %H:%M:%S")
        end_time = datetime.strptime(daily_time["_source"]["end_time"], "%Y-%m-%dT%H:%M:%S.%fZ").strftime("%Y-%m-%d %H:%M:%S")
    
        # start_time = daily_time["_source"]["start_time"]
        # end_time = daily_time["_source"]["end_time"]
        led = daily_time["_source"]["led_state"]

        daily_on_off_times.append({
            "date": date,
            "start_time": start_time,
            "end_time": end_time,
            "led": led
        })

    return daily_on_off_times


@login_required
def led_view(request):
    selected_date = request.GET.get('date')
    if selected_date:
        selected_date = datetime.strptime(selected_date, "%Y-%m-%d").date()

    if TEST_DATA_ENABLED:
        on_off_times = daily_on_off_sum_offline(selected_date)
        daily_times = daily_on_off_times_offline(selected_date)
    else:
        on_off_times = get_onoff_daily_minutes(es_client, selected_date)
        daily_times = get_daily_minutes(es_client, selected_date)

    # print(on_off_times)
    # print(daily_times)

    return render(request, 'led.html', {'daily_times': daily_times, 'on_off_times': on_off_times, 'selected_date': selected_date})
