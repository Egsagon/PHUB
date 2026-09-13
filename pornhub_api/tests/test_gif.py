import os
import pytest
from base_api import DownloadConfigRAW

from pornhub_api import Client
from pornhub_api.api import GIF


@pytest.fixture
def client():
    return Client()


@pytest.mark.asyncio
async def test_gif(client, tmp_path):
    gif = await client.get_gif("https://www.pornhub.com/gif/54402301", load_html=True)
    assert isinstance(gif.title, str) and len(gif.title) > 0
    assert isinstance(gif.thumbnail, str) and len(gif.thumbnail) > 0
    assert isinstance(gif.publish_date, str) and len(gif.publish_date) > 0
    assert isinstance(gif.content_url, str) and len(gif.content_url) > 0
    assert isinstance(gif.tags, dict) and len(gif.tags) > 0
    assert isinstance(gif.vote_count, str)
    assert isinstance(gif.vote_percentage, str)

    # New attributes
    assert gif.gif_id == "54402301"
    assert gif.author_name == "Chappy1918"
    assert gif.author_link == "https://www.pornhub.com/users/chappy1918"
    assert gif.author_id == "2176853831"
    assert gif.source_video_url is not None and "viewkey=684c544e1f724" in gif.source_video_url
    assert isinstance(gif.source_video_title, str) and len(gif.source_video_title) > 0
    assert gif.source_video_timestamp == "20:20"
    assert isinstance(gif.tag_names, list) and len(gif.tag_names) > 0
    assert isinstance(gif.token, str) and len(gif.token) > 0
    assert isinstance(gif.mp4_url, str) and gif.mp4_url.startswith("http")
    assert isinstance(gif.gif_url, str) and gif.gif_url.startswith("http")
    assert gif.embed_url == "https://www.pornhub.com/embedgif/54402301"

    # Helper methods
    author = await gif.get_author()
    assert author is not None
    assert author.url == gif.author_link

    source_video = await gif.get_source_video()
    assert source_video is not None
    assert source_video.url == gif.source_video_url

    # Download
    config = DownloadConfigRAW(quality="best", path=str(tmp_path))
    assert await gif.download(configuration=config) is True


def test_gif_extract_html_sample(client):
    sample_html = """
    <div id="gifWrap" class="clearfix" data-link-to="gif54402301" data-gif-id="gif54402301" data-is-tablet="0">
        <div class="gifColumnLeft float-left">
            <div id="gifImageSection">
                <div id="js-gifToWebm" class="centerImage notModal"
                     data-gif="https://el2.phncdn.com/gif/54402301.gif"
                     data-mp4="https://el2.phncdn.com/pics/gifs/054/402/301/54402301a.mp4"
                     data-webm="https://el2.phncdn.com/pics/gifs/054/402/301/54402301a.webm"
                     data-gif-title="Reverse cowgirl"
                     data-fallback="https://el2.phncdn.com/pics/gifs/054/402/301/54402301a.mp4">
                    <div class="gifTitle">
                        <h1>Reverse cowgirl Gif</h1>
                    </div>
                    <ul class="votingWrap ratingsContentClass clearfix">
                        <li class="float-left tooltipTrig alpha">
                            <button id="voteUp" data-current="29" data-vote-url="/api/v1/gif/54402301/rate?token=SECRET_TOKEN">
                                <span class="ph-icon-thumb-up thumbsUpIcon"></span>
                            </button>
                        </li>
                        <li class="barContainerWrap float-left clearfix">
                            <div class="barContainer">
                                <div class="votePercentage"><span>97</span>%</div>
                                <div class="voteCount">(<span class="voteCountNumber">30</span> votes)</div>
                                <input type="hidden" id="currentId" value="54402301">
                                <input type="hidden" id="votesUp" value="29">
                                <input type="hidden" id="votesDown" value="1">
                            </div>
                        </li>
                        <li class="float-left tooltipTrig">
                            <button id="voteDown" data-current="1" data-vote-url="/api/v1/gif/54402301/rate?token=SECRET_TOKEN"></button>
                        </li>
                        <li class="float-right gifViews omega">
                            <strong>9,682 views</strong>
                        </li>
                    </ul>
                    <div class="shareLinksWrapper clearfix">
                        <input type="text" id="directlink" name="directlink" value="https://www.pornhub.com/embedgif/54402301" readonly="">
                    </div>
                </div>
            </div>
            <div id="gifInfoSection" class="clearfix">
                <div class="sourceTagDiv">
                    <div class="bottomMargin">
                        From this video: <a href="/view_video.php?viewkey=684c544e1f724">Sample Video Title</a>
                        <span class="linkBetween">&nbsp;at&nbsp;</span><a href="javascript:void(0)" class="directLink tstamp">20:20</a>
                    </div>
                    <div class="clearfix">
                        <ul class="tagList clearfix">
                            <li><a href="/gifs/search?search=reverse+cowgirl" class="tagText">reverse cowgirl gifs</a></li>
                            <li><a href="/gifs/search?search=romantic+sex" class="tagText">romantic sex</a></li>
                        </ul>
                    </div>
                    <div class="bottomMargin">
                        Created by:
                        <div class="usernameWrap clearfix" data-type="user" data-userid="2176853831">
                            <a href="/users/chappy1918" title="Chappy1918">Chappy1918</a>
                        </div>
                        <div class="added">4 months ago</div>
                    </div>
                </div>
            </div>
        </div>
    </div>
    """
    gif = GIF(core=client.core, url="https://www.pornhub.com/gif/54402301")
    data = gif._extract_html(sample_html)

    assert data["title"] == "Reverse cowgirl Gif"
    assert data["gif_id"] == "54402301"
    assert data["content_url"] == "https://el2.phncdn.com/pics/gifs/054/402/301/54402301a.mp4"
    assert data["mp4_url"] == "https://el2.phncdn.com/pics/gifs/054/402/301/54402301a.mp4"
    assert data["webm_url"] == "https://el2.phncdn.com/pics/gifs/054/402/301/54402301a.webm"
    assert data["gif_url"] == "https://el2.phncdn.com/gif/54402301.gif"
    assert data["thumbnail"] == "https://el2.phncdn.com/gif/54402301.gif"
    assert data["publish_date"] == "4 months ago"
    assert data["views"] == "9,682 views"
    assert data["vote_count"] == "30"
    assert data["vote_percentage"] == "97"
    assert data["votes_up"] == "29"
    assert data["votes_down"] == "1"
    assert data["author_name"] == "Chappy1918"
    assert data["author_link"] == "https://www.pornhub.com/users/chappy1918"
    assert data["author_id"] == "2176853831"
    assert data["source_video_url"] == "https://www.pornhub.com/view_video.php?viewkey=684c544e1f724"
    assert data["source_video_title"] == "Sample Video Title"
    assert data["source_video_timestamp"] == "20:20"
    assert data["tag_names"] == ["reverse cowgirl gifs", "romantic sex"]
    assert data["tags"] == {
        "reverse cowgirl gifs": "/gifs/search?search=reverse+cowgirl",
        "romantic sex": "/gifs/search?search=romantic+sex",
    }
    assert data["token"] == "SECRET_TOKEN"
    assert data["embed_url"] == "https://www.pornhub.com/embedgif/54402301"


def test_gif_extract_html_fallbacks(client):
    gif = GIF(core=client.core, url="https://www.pornhub.com/gif/sample-gif-title")
    data = gif._extract_html("")

    assert data["title"] == "Sample Gif Title"
    assert data["content_url"] is None
    assert data["thumbnail"] is None
    assert data["publish_date"] is None
    assert data["source_video_url"] is None
    assert data["author_name"] is None
    assert data["tags"] == {}
    assert data["tag_names"] == []
