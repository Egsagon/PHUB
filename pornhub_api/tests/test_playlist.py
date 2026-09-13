import pytest

from pornhub_api import Client, User

@pytest.fixture
def client():
    return Client()

@pytest.mark.asyncio
async def test_playlist(client):
    playlist = await client.get_playlist("https://www.pornhub.com/playlist/119820351")
    assert isinstance(playlist.title, str) and len(playlist.title) > 0
    assert isinstance(playlist.tags, dict) and len(playlist.tags) > 0
    assert isinstance(playlist.token, str) and len(playlist.token) > 0
    assert isinstance(playlist.playlist_id, str) and len(playlist.playlist_id) > 0
    assert isinstance(playlist.views, str) and len(playlist.views) > 0
    assert isinstance(playlist.unavailable_videos, int)
    assert isinstance(playlist.rating_percent, str) and len(playlist.rating_percent) > 0
    assert isinstance(playlist.video_count, str) and len(str(playlist.video_count)) > 0
    assert isinstance(playlist.description, str) and len(playlist.description) > 0
    assert playlist.description != "Description:"
    assert isinstance(playlist.likes, str)
    assert isinstance(playlist.dislikes, str)
    assert isinstance(playlist.author_name, str) and len(playlist.author_name) > 0
    assert isinstance(playlist.author_id, str) and len(playlist.author_id) > 0
    assert isinstance(playlist.status, str)
    assert isinstance(playlist.tag_names, list) and len(playlist.tag_names) > 0
    assert isinstance(playlist.author, User)
    assert isinstance(await playlist.get_author(), User)

    idx = 0
    async for result in playlist.get_videos():
        idx += 1
        assert isinstance(result.unwrap().title, str)

        if idx == 5:
            break


def test_playlist_extract_html_fallback(client):
    from pornhub_api.api import Playlist

    sample_html = """
    <div id="playlistWrapper">
        <div id="playlistTopHeader">
            <h1 id="watchPlaylist" class="playlistTitle">Big Natural Tits</h1>
            <span class="rating up">90%</span>
        </div>
        <div id="viewsRatings">
            <div class="views"><span class="count">3,622,585</span> views</div>
            <div class="votes-count-container">
                <span class="percent">90%</span>
                <span class="votesUp">6800</span>
                <span class="votesDown">769</span>
            </div>
        </div>
        <div class="aboutInfo" id="js-aboutPlaylistTabView">
            <span>From: </span>
            <div class="usernameWrap" data-type="user" data-userid="934899081">
                <a href="/users/germanonex" title="GerManOneX">GerManOneX</a>
                - 1995 videos
            </div>
            <div id="tagSection">
                <div class="tagsWrap js-tagsWrap">
                    <span>Tags: </span>
                    <a data-label="tag" class="isTag" href="/video?c=8"><span>big tits</span></a>,
                    <a data-label="tag" class="isTag" href="/video/search?search=milf"><span>milf</span></a>
                </div>
                <p class="description js-playlistDescription">
                    <span>Description: </span> Great playlist of natural tits
                </p>
            </div>
        </div>
        <form id="edit-pl-form">
            <input name="edit-pl-id" id="js-editPlaylistId" type="hidden" value="119820351">
            <input id="js-status" name="status" type="hidden" value="public_albums">
        </form>
        <p style="color: red;">Number of unavailable videos that are hidden: 181</p>
        <input type="text" data-token="MTc4ODk3MDczNvR0jsauD_JqSJ26KQ7F41nsGHVZFlXoEFLAQLT4DnpmGeqlla47fOWzQ1O2RqzsBhHyH6w_REWbhEkGqyItGhU.">
        <ul id="videoPlaylist">
            <li class="pcVideoListItem">
                <a href="/view_video.php?viewkey=ph5d26a36574f6c&pkey=119820351" class="linkVideoThumb">
                    <img data-image="https://ei.phncdn.com/videos/test.jpg" />
                </a>
            </li>
        </ul>
    </div>
    """
    pl = Playlist(url="https://www.pornhub.com/playlist/119820351", core=client.core)
    extracted = pl._extract_html(sample_html)

    assert extracted["playlist_id"] == "119820351"
    assert extracted["token"] == "MTc4ODk3MDczNvR0jsauD_JqSJ26KQ7F41nsGHVZFlXoEFLAQLT4DnpmGeqlla47fOWzQ1O2RqzsBhHyH6w_REWbhEkGqyItGhU."
    assert extracted["title"] == "Big Natural Tits"
    assert extracted["views"] == "3,622,585"
    assert extracted["rating_percent"] == "90%"
    assert extracted["likes"] == "6800"
    assert extracted["dislikes"] == "769"
    assert extracted["author_link"] == "https://www.pornhub.com/users/germanonex"
    assert extracted["author_name"] == "GerManOneX"
    assert extracted["author_id"] == "934899081"
    assert extracted["video_count"] == "1995"
    assert extracted["description"] == "Great playlist of natural tits"
    assert extracted["unavailable_videos"] == 181
    assert "big tits" in extracted["tags"]
    assert "milf" in extracted["tags"]
    assert extracted["status"] == "public"
    assert extracted["thumbnail"] == "https://ei.phncdn.com/videos/test.jpg"
    assert extracted["first_video_url"] == "https://www.pornhub.com/view_video.php?viewkey=ph5d26a36574f6c&pkey=119820351"
