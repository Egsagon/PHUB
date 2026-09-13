import pytest
from base_api import DownloadConfigHLS

from pornhub_api import Client

@pytest.fixture
def client():
    return Client()

@pytest.mark.asyncio
async def test_video(client):
    client = Client()
    # By default this uses HubTraffic API
    video = await client.get_video("https://www.pornhub.com/view_video.php?viewkey=ph618ed49fbee04", load_api=True, load_html=True)

    # These should be available via API data without HTML
    assert isinstance(video.title, str) and len(video.title) > 3
    assert isinstance(video.publish_date, str) and len(video.publish_date) > 1
    assert isinstance(video.duration, int)
    assert isinstance(video.likes, int)
    assert isinstance(video.thumbnail, str)

    assert isinstance(video.available_qualities, list) and len(video.available_qualities) > 0
    assert isinstance(video.is_vertical, bool)
    assert isinstance(video.is_video_unavailable, bool)
    assert isinstance(video.is_vr, bool)
    assert isinstance(video.is_hd, bool)
    assert isinstance(video.author_thumbnail, str) and len(video.author_thumbnail) > 0
    # After HTML fetch, these might be dicts if from scrape or list if from API
    assert isinstance(video.categories, (dict, list))
    assert isinstance(video.tags, (dict, list))
    assert isinstance(video.pornstars, list)
    assert isinstance(video.segment, str)
    assert isinstance(video.is_premium, bool)
    assert isinstance(video.description, str)
    assert isinstance(video.m3u8_base_url, str)
    assert isinstance(video.is_video_unavailable_in_your_country, bool)

    config = DownloadConfigHLS(quality="best", return_report=True, path="./")
    stuff = await video.download(config)
    assert stuff["status"] == "completed"


def test_video_extract_html_fallback():
    from pornhub_api.api import Video

    sample_html = """
    <div class="video-wrapper">
        <script>
        var VIDEO_SHOW = {
            "videoTitle": "Double D Breasted Babe Ella Knox Gets a Hand Delivered Cum Load to her Huge Tits",
            "placeholder": "https://ei.phncdn.com/videos/test.jpg",
            "isPremium": 0,
            "segment": "straight",
            "vr": "{\\"enabled\\":0}"
        };
        </script>
    </div>
    """
    extracted = Video._extract_html(sample_html, "https://www.pornhub.com/view_video.php?viewkey=685380fd4044d")

    assert extracted["title"] == "Double D Breasted Babe Ella Knox Gets a Hand Delivered Cum Load to her Huge Tits"
    assert extracted["thumbnail"] == "https://ei.phncdn.com/videos/test.jpg"
    assert extracted["segment"] == "straight"
    assert extracted["is_premium"] is False
    assert extracted["is_vr"] is False
    assert extracted["is_video_unavailable"] is False
    assert extracted["duration"] is None
    assert extracted["available_qualities"] == []
    assert extracted["categories"] == []
    assert extracted["tags"] == []
    assert extracted["pornstars"] == []


