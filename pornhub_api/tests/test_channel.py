import pytest
from pornhub_api import Client
from pornhub_api.api import Channel

@pytest.fixture
def client() -> Client:
    return Client()


@pytest.mark.asyncio
async def test_channel(client):
    channel = await client.get_channel("https://www.pornhub.com/channels/brazzers/", load_html=True)
    assert channel.name == "Brazzers"
    assert isinstance(channel.description, str) and len(channel.description) > 0
    assert channel.rank == "1"
    assert isinstance(channel.join_date, str) and len(channel.join_date) > 0
    assert isinstance(channel.website, str) and len(channel.website) > 0
    assert channel.website_name == "Brazzers.com"
    assert channel.is_award_winner is True
    assert channel.is_content_partner is True
    assert channel.channel_id == "4101"
    assert isinstance(channel.token, str) and len(channel.token) > 0
    assert isinstance(channel.avatar_url, str) and channel.avatar_url.startswith("http")
    assert isinstance(channel.cover_url, str) and channel.cover_url.startswith("http")
    assert channel.owner_name == "Brazzers"
    assert channel.user_link == "https://www.pornhub.com/users/brazzers"
    assert isinstance(channel.subscribers, str) and len(channel.subscribers) > 0
    assert "SUBSCRIBERS" not in channel.subscribers
    assert isinstance(channel.total_videos, str) and len(channel.total_videos) > 0
    assert "VIDEOS" not in channel.total_videos
    assert isinstance(channel.video_views, str) and len(channel.video_views) > 0
    assert "VIDEO VIEWS" not in channel.video_views
    assert isinstance(channel.badges, list) and "Content Partner" in channel.badges
    assert isinstance(channel.pornstars, list) and len(channel.pornstars) > 0

    user = await channel.get_user()
    assert user is not None
    assert isinstance(user.about, str) and len(user.about) > 0


def test_channel_extract_html_sample(client):
    sample_html = """
    <section id="channelsProfile">
        <div class="header clearfix">
            <div class="cover clearfix">
                <section id="topProfileHeader">
                    <div id="coverPicture">
                        <img id="coverPictureDefault" src="https://ei.phncdn.com/pics/sites/0006/5239/1351/cover323925/(m=maeRSaaGqaq)(mh=tE5xoYEfRtXpNV-d)1323x270.jpg" alt="Latina Milf cover" width="100%" data-title="" title="">
                    </div>
                    <div class="avatar" id="avatarPicture">
                        <div class="previewAvatarPicture">
                            <img id="getAvatar" src="https://ei.phncdn.com/pics/sites/0006/5239/1351/avatar109065/(m=eidYGe)(mh=Dm2zvF_nNx__6SFG)200x200.jpg" class="jcrop-preview" alt="Latina Milf Profile Picture" data-title="" title="">
                        </div>
                    </div>
                </section>
            </div>
            <div class="bottomExtendedWrapper clearfix">
                <div class="floatLeft titleWrapper">
                    <div class="title floatLeft">
                        <h1>
                            Latina Milf                        
                            <span class="bg-channel-badge producer-icon userBadges spriteUi tooltipTrig channel-icon main-sprite searchPageIcon" data-title="Content Partner"></span>
                        </h1>
                    </div>
                    <div class="userButtons subscribe floatLeft js-channelSubscribe">
                        <div class="subscribeButton js-cpp-subscribe-btn updatedStyledBtn js-animatedSubscribeBtn subscribe subscribe_65651" data-button-id="subscribe_65651" data-glow-init="1">
                            <button class="buttonBase" data-id="65651" data-login="0" data-subscribe-url="/channel/subscribe_add_json?id=65651&amp;token=MTc4ODk3MTI4OWUb84IZXhvJB7XhTkdvoEFPu0XGwGwOYCv_i7_K5_VgHetfIeFrmskm7IPWIJ9RLpTVGy-6_OKKTcXutaVTen8." data-unsubscribe-url="/channel/subscribe_remove_json?id=65651&amp;token=MTc4ODk3MTI4OWUb84IZXhvJB7XhTkdvoEFPu0XGwGwOYCv_i7_K5_VgHetfIeFrmskm7IPWIJ9RLpTVGy-6_OKKTcXutaVTen8." data-subscribed="0" type="button" data-refresh="0" data-updated-icon-mode="modern">
                                <span class="buttonLabel">Subscribe</span>
                            </button>
                        </div>
                    </div>
                </div>
                <div id="stats" class="floatRight">
                    <div class="info floatRight">90,951,709 <br><span>VIDEO VIEWS</span></div>
                    <div class="info floatRight">124,385 <br><span>SUBSCRIBERS</span></div>
                    <div class="info floatRight">905 <br><span>VIDEOS</span></div>
                    <div class="info floatRight">34 <br><span>RANK</span></div>
                </div>
            </div>
        </div>
        <div class="cdescriptions">
            <p class="joined">Your adoration of the Latina MILF goddess has a new home. All of your favorite stars are here as well as a steady stream of pretty new faces all waiting to be adorned with fresh jizz.</p>
            <p class="joined"><span class="channelInfoHeadlines">JOINED</span> <span>3 years ago</span></p>
            <p class="joined">
                <span class="channelInfoHeadlines">WEBSITE</span>
                <a href="https://landing.latinamilf.com/?ats=eyJhIjo4NzUyLCJjIjo0MzMxOTAwNSwibiI6MTI4LCJzIjo3MjgsImUiOjExMDM0LCJwIjoyfQ==&amp;atc=Autocampaign_Default" target="_blank" rel="noopener nofollow">latinamilf.com</a>
            </p>
            <p class="joined">
                <span class="channelInfoHeadlines">BY</span>
                <a href="/users/letsdoeit" target="_blank">LetsDoeIt</a>
            </p>
        </div>
        <ul class="channelPornstars">
            <li class="pornstarLi performerCard alpha">
                <div class="wrap">
                    <a href="/pornstar/kenia-music">
                        <img src="https://ei.phncdn.com/avatar.jpg" alt="Kenia Music">
                    </a>
                </div>
            </li>
            <li class="pornstarLi performerCard">
                <div class="wrap">
                    <a href="/pornstar/samie-duchamp">
                        <img src="https://ei.phncdn.com/avatar2.jpg" alt="Samie Duchamp">
                    </a>
                </div>
            </li>
            <li class="pornstarLi performerCard">
                <div class="wrap">
                    <a href="/pornstar/niky-bimbodoll">
                        <img src="https://ei.phncdn.com/avatar3.jpg" alt="NIKY BIMBODOLL">
                    </a>
                </div>
            </li>
            <li class="pornstarLi performerCard omega">
                <div class="wrap">
                    <a href="/pornstar/jimmy-bud">
                        <img src="https://ei.phncdn.com/avatar4.jpg" alt="Jimmy Bud">
                    </a>
                </div>
            </li>
        </ul>
    </section>
    """
    ch = Channel(core=client.core, url="https://www.pornhub.com/channels/latina-milf")
    data = ch._extract_html(sample_html)

    assert data["name"] == "Latina Milf"
    assert data["channel_id"] == "65651"
    assert data["token"] == "MTc4ODk3MTI4OWUb84IZXhvJB7XhTkdvoEFPu0XGwGwOYCv_i7_K5_VgHetfIeFrmskm7IPWIJ9RLpTVGy-6_OKKTcXutaVTen8."
    assert data["video_views"] == "90,951,709"
    assert data["subscribers"] == "124,385"
    assert data["total_videos"] == "905"
    assert data["rank"] == "34"
    assert data["join_date"] == "3 years ago"
    assert data["website"] == "https://landing.latinamilf.com/?ats=eyJhIjo4NzUyLCJjIjo0MzMxOTAwNSwibiI6MTI4LCJzIjo3MjgsImUiOjExMDM0LCJwIjoyfQ==&atc=Autocampaign_Default"
    assert data["website_name"] == "latinamilf.com"
    assert data["owner_name"] == "LetsDoeIt"
    assert data["user_link"] == "https://www.pornhub.com/users/letsdoeit"
    assert data["cover_url"] == "https://ei.phncdn.com/pics/sites/0006/5239/1351/cover323925/(m=maeRSaaGqaq)(mh=tE5xoYEfRtXpNV-d)1323x270.jpg"
    assert data["avatar_url"] == "https://ei.phncdn.com/pics/sites/0006/5239/1351/avatar109065/(m=eidYGe)(mh=Dm2zvF_nNx__6SFG)200x200.jpg"
    assert data["badges"] == ["Content Partner"]
    assert data["is_award_winner"] is False
    assert data["is_content_partner"] is True
    assert data["pornstars"] == ["Kenia Music", "Samie Duchamp", "NIKY BIMBODOLL", "Jimmy Bud"]
    assert "Your adoration of the Latina MILF goddess" in data["description"]


def test_channel_extract_html_fallback(client):
    ch = Channel(core=client.core, url="https://www.pornhub.com/channels/awesome-studio")
    data = ch._extract_html("<html><body></body></html>")

    assert data["name"] == "Awesome Studio"
    assert data["video_views"] is None
    assert data["subscribers"] is None
    assert data["total_videos"] is None
    assert data["rank"] is None
    assert data["description"] is None
    assert data["join_date"] is None
    assert data["website"] is None
    assert data["user_link"] is None
    assert data["channel_id"] is None
    assert data["token"] is None
    assert data["avatar_url"] is None
    assert data["cover_url"] is None
    assert data["owner_name"] is None
    assert data["badges"] == []
    assert data["pornstars"] == []
    assert data["is_award_winner"] is False
    assert data["is_content_partner"] is False