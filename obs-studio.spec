# TODO: AJA (BR: libajantv2)
#
# Conditional build:
%bcond_with	aja	# AJA NTV2 support
%bcond_without	jack	# JACK support
%bcond_with	qt5	# Qt 5 instead of Qt 6
%bcond_with	webrtc	# Build WebRTC output plugin (R: LibDataChannel)

%ifnarch %{x8664}
# plugins/aja/cmake/legacy.cmake: "aja support not enabled (32-bit not supported)."
%undefine	with_aja
%endif
Summary:	OBS Studio - live streaming and screen recording software
Summary(pl.UTF-8):	OBS Studio - oprogramowanie do przesyłania strumieni na żywo i nagrywania ekranu
Name:		obs-studio
Version:	31.0.0
Release:	1
License:	GPL v2+
Group:		X11/Applications/Multimedia
#Source0Download: https://github.com/obsproject/obs-studio/releases
Source0:	https://github.com/jp9000/obs-studio/archive/%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	7dd7edb0c4e159b1c78c5ce24a3d746b
Patch0:		disable-missing-plugins.patch
Patch1:		size_t.patch
Patch2:		x32.patch
Patch3:		sign-compare.patch
Patch4:		x11-linkage.patch
Patch5:		luajit-lua52.patch
URL:		https://obsproject.com/
BuildRequires:	ImageMagick-devel
BuildRequires:	OpenGL-GLX-devel
BuildRequires:	alsa-lib-devel
BuildRequires:	cmake >= 3.16
BuildRequires:	curl-devel
BuildRequires:	dbus-devel
# avcodec avfilter avdevice avutil swscale avformat swresample
BuildRequires:	ffmpeg-devel
BuildRequires:	fontconfig-devel
BuildRequires:	freetype-devel >= 2
BuildRequires:	glib2-devel >= 2.0
%{?with_jack:BuildRequires:	jack-audio-connection-kit-devel}
BuildRequires:	jansson-devel >= 2.5
%{?with_aja:BuildRequires:	libajantv2-devel}
BuildRequires:	libdrm-devel
BuildRequires:	librist-devel
BuildRequires:	libstdc++-devel >= 6:4.7
BuildRequires:	libv4l-devel
BuildRequires:	libva-devel
BuildRequires:	libvpl-devel
BuildRequires:	libx264-devel
# xcb xcb-composite xcb-randr xcb-shm xcb-xfixes xcb-xinerama
BuildRequires:	libxcb-devel
%ifnarch x32
BuildRequires:	luajit-devel
%endif
BuildRequires:	mbedtls-devel
BuildRequires:	nv-codec-headers
BuildRequires:	pciutils-devel
BuildRequires:	pipewire-devel >= 0.3.33
BuildRequires:	pkgconfig
BuildRequires:	pulseaudio-devel
BuildRequires:	python3-devel >= 1:3.2
BuildRequires:	rpmbuild(macros) >= 1.605
BuildRequires:	speexdsp-devel
BuildRequires:	srt-devel
BuildRequires:	swig-python >= 2
BuildRequires:	udev-devel
BuildRequires:	uthash-devel
BuildRequires:	vlc-devel
# wayland-client
BuildRequires:	wayland-devel
BuildRequires:	wayland-egl-devel
BuildRequires:	xorg-lib-libX11-devel
BuildRequires:	zlib-devel
%if %{with qt5}
BuildRequires:	Qt5Core-devel >= 5
BuildRequires:	Qt5Gui-devel >= 5
BuildRequires:	Qt5Network-devel >= 5
BuildRequires:	Qt5Svg-devel >= 5
BuildRequires:	Qt5Widgets-devel >= 5
BuildRequires:	Qt5Xml-devel >= 5
BuildRequires:	qt5-build >= 5
BuildRequires:	qt5-qmake >= 5
%else
BuildRequires:	Qt6Core-devel >= 6
BuildRequires:	Qt6Gui-devel >= 6
BuildRequires:	Qt6Network-devel >= 6
BuildRequires:	Qt6Svg-devel >= 6
BuildRequires:	Qt6Widgets-devel >= 6
BuildRequires:	Qt6Xml-devel >= 6
BuildRequires:	qt6-build >= 6
BuildRequires:	qt6-qmake >= 6
%endif
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_noautoprovfiles	%{_libdir}/obs-plugins

# symbols from libm confuse the checker
%define		skip_post_check_so	libobs.so.*

%description
OBS Studio is software designed for capturing, compositing, encoding,
recording, and streaming video content, efficiently.

%description -l pl.UTF-8
OBS Studio to oprogramowanie służące do wydajnego przechwytywania,
składania, kodowania, nagrywania i przesyłania treści wideo.

%package devel
Summary:	Header files for OBS Studio
Summary(pl.UTF-8):	Pliki nagłówkowe OBS Studio
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header files for OBS Studio.

%description devel -l pl.UTF-8
Pliki nagłówkowe OBS Studio.

%prep
%setup -q
%patch -P 0 -p1
%patch -P 1 -p1
%patch -P 2 -p1
%patch -P 3 -p1
%patch -P 4 -p1
%patch -P 5 -p1

%build
export OBS_MULTIARCH_SUFFIX="%(echo "%{_lib}" | sed -e 's/^lib//')"
%cmake -B build \
	-DCMAKE_INSTALL_BINDIR:PATH=bin \
	-DCMAKE_INSTALL_INCLUDEDIR:PATH=include \
	-DCMAKE_INSTALL_DATAROOTDIR:PATH=share \
	-DCMAKE_INSTALL_DATADIR:PATH=share \
	-DCMAKE_INSTALL_LIBDIR:PATH=%{_lib} \
	-DCMAKE_SKIP_RPATH=1 \
	-DBUILD_BROWSER=OFF \
	-DCALM_DEPRECATION=ON \
	%{!?with_aja:-DENABLE_AJA=OFF} \
	%{?with_jack:-DENABLE_JACK=ON} \
%ifarch x32
	-DENABLE_SCRIPTING_LUA=OFF \
%endif
	%{!?with_webrtc:-DENABLE_WEBRTC=OFF} \
	-DOBS_VERSION_OVERRIDE=%{version} \
	-DQT_VERSION=%{?with_qt5:5}%{!?with_qt5:6} \
	-DUNIX_STRUCTURE=1

%{__make} -C build

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -C build install/fast \
        DESTDIR=$RPM_BUILD_ROOT

builddir="$(pwd)"

cd $RPM_BUILD_ROOT
reldatadir="$(echo %{_datadir} | sed -e 's,^/,,')"
for f in $reldatadir/obs/obs-studio/locale/??*-??*.ini $reldatadir/obs/obs-plugins/*/locale/??*-??*.ini ; do
	locale="$(basename "$f" .ini | tr - _)"
	case "$locale" in
	  en_US)
		loctag=""
		;;
	  pt_BR|zh_CN|zh_TW)
		loctag="%lang($locale) "
		;;
	  *)
		# this rule covers also conversion of bogus Serbian codes to "sr": "sr_CS" (actually sr_RS@latin), "sr_SP" (actually sr_RS, cyrillic)
		loctag="%lang(${locale%_??}) "
		;;
	esac
	echo "${loctag}/$f"
done > "$builddir/%{name}.lang"

# dir guard
%{__rm} $RPM_BUILD_ROOT%{_datadir}/obs/obs-plugins/{decklink-captions,decklink-output-ui}/.keepme
%{__rm} $RPM_BUILD_ROOT%{_datadir}/obs/obs-plugins/linux-pipewire/.gitkeep

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS README.rst
%attr(755,root,root) %{_bindir}/obs
%attr(755,root,root) %{_bindir}/obs-ffmpeg-mux
%attr(755,root,root) %{_bindir}/obs-nvenc-test
%attr(755,root,root) %{_libdir}/libobs-frontend-api.so.30
%attr(755,root,root) %ghost %{_libdir}/libobs-frontend-api.so.0
%attr(755,root,root) %{_libdir}/libobs-opengl.so.30
%attr(755,root,root) %{_libdir}/libobs.so.30
%attr(755,root,root) %ghost %{_libdir}/libobs.so.0
%attr(755,root,root) %{_libdir}/libobs-scripting.so.30

%dir %{_libdir}/obs-plugins
%attr(755,root,root) %{_libdir}/obs-plugins/decklink-captions.so
%attr(755,root,root) %{_libdir}/obs-plugins/decklink-output-ui.so
%attr(755,root,root) %{_libdir}/obs-plugins/decklink.so
%attr(755,root,root) %{_libdir}/obs-plugins/frontend-tools.so
%attr(755,root,root) %{_libdir}/obs-plugins/image-source.so
%attr(755,root,root) %{_libdir}/obs-plugins/linux-alsa.so
%attr(755,root,root) %{_libdir}/obs-plugins/linux-capture.so
%if %{with jack}
%attr(755,root,root) %{_libdir}/obs-plugins/linux-jack.so
%endif
%attr(755,root,root) %{_libdir}/obs-plugins/linux-pipewire.so
%attr(755,root,root) %{_libdir}/obs-plugins/linux-pulseaudio.so
%attr(755,root,root) %{_libdir}/obs-plugins/linux-v4l2.so
%attr(755,root,root) %{_libdir}/obs-plugins/obs-ffmpeg.so
%attr(755,root,root) %{_libdir}/obs-plugins/obs-filters.so
%attr(755,root,root) %{_libdir}/obs-plugins/obs-nvenc.so
%attr(755,root,root) %{_libdir}/obs-plugins/obs-outputs.so
%attr(755,root,root) %{_libdir}/obs-plugins/obs-qsv11.so
%attr(755,root,root) %{_libdir}/obs-plugins/obs-transitions.so
%attr(755,root,root) %{_libdir}/obs-plugins/obs-vst.so
%attr(755,root,root) %{_libdir}/obs-plugins/obs-x264.so
%attr(755,root,root) %{_libdir}/obs-plugins/rtmp-services.so
%attr(755,root,root) %{_libdir}/obs-plugins/text-freetype2.so
%attr(755,root,root) %{_libdir}/obs-plugins/vlc-video.so
%dir %{_libdir}/obs-scripting
%ifnarch x32
%attr(755,root,root) %{_libdir}/obs-scripting/obslua.so
%endif
%attr(755,root,root) %{_libdir}/obs-scripting/_obspython.so
%attr(755,root,root) %{_libdir}/obs-scripting/obspython.py

%{_datadir}/metainfo/com.obsproject.Studio.metainfo.xml
%{_desktopdir}/com.obsproject.Studio.desktop
%{_iconsdir}/hicolor/*x*/apps/com.obsproject.Studio.png
%{_iconsdir}/hicolor/scalable/apps/com.obsproject.Studio.svg

%dir %{_datadir}/obs
%{_datadir}/obs/libobs
%dir %{_datadir}/obs/obs-plugins
%dir %{_datadir}/obs/obs-studio
%{_datadir}/obs/obs-studio/OBSPublicRSAKey.pem
%{_datadir}/obs/obs-studio/authors
%{_datadir}/obs/obs-studio/images
%{_datadir}/obs/obs-studio/license
%dir %{_datadir}/obs/obs-studio/locale
%{_datadir}/obs/obs-studio/themes
%{_datadir}/obs/obs-studio/locale.ini

%dir %{_datadir}/obs/obs-plugins/decklink
%dir %{_datadir}/obs/obs-plugins/decklink/locale

%dir %{_datadir}/obs/obs-plugins/frontend-tools
%dir %{_datadir}/obs/obs-plugins/frontend-tools/locale
%dir %{_datadir}/obs/obs-plugins/frontend-tools/scripts
%{_datadir}/obs/obs-plugins/frontend-tools/scripts/*.lua
%{_datadir}/obs/obs-plugins/frontend-tools/scripts/*.py
%{_datadir}/obs/obs-plugins/frontend-tools/scripts/clock-source

%dir %{_datadir}/obs/obs-plugins/image-source
%dir %{_datadir}/obs/obs-plugins/image-source/locale

%dir %{_datadir}/obs/obs-plugins/linux-alsa
%dir %{_datadir}/obs/obs-plugins/linux-alsa/locale

%dir %{_datadir}/obs/obs-plugins/linux-capture
%dir %{_datadir}/obs/obs-plugins/linux-capture/locale

%dir %{_datadir}/obs/obs-plugins/linux-pipewire
%dir %{_datadir}/obs/obs-plugins/linux-pipewire/locale

%dir %{_datadir}/obs/obs-plugins/linux-pulseaudio
%dir %{_datadir}/obs/obs-plugins/linux-pulseaudio/locale

%dir %{_datadir}/obs/obs-plugins/linux-v4l2
%dir %{_datadir}/obs/obs-plugins/linux-v4l2/locale

%dir %{_datadir}/obs/obs-plugins/obs-ffmpeg
%dir %{_datadir}/obs/obs-plugins/obs-ffmpeg/locale

%dir %{_datadir}/obs/obs-plugins/obs-filters
%{_datadir}/obs/obs-plugins/obs-filters/*.effect
%{_datadir}/obs/obs-plugins/obs-filters/LUTs
%dir %{_datadir}/obs/obs-plugins/obs-filters/locale

%dir %{_datadir}/obs/obs-plugins/obs-outputs
%dir %{_datadir}/obs/obs-plugins/obs-outputs/locale

%dir %{_datadir}/obs/obs-plugins/obs-transitions
%{_datadir}/obs/obs-plugins/obs-transitions/*.effect
%{_datadir}/obs/obs-plugins/obs-transitions/luma_wipes
%dir %{_datadir}/obs/obs-plugins/obs-transitions/locale

%dir %{_datadir}/obs/obs-plugins/obs-vst
%dir %{_datadir}/obs/obs-plugins/obs-vst/locale

%dir %{_datadir}/obs/obs-plugins/obs-x264
%dir %{_datadir}/obs/obs-plugins/obs-x264/locale

%dir %{_datadir}/obs/obs-plugins/rtmp-services
%{_datadir}/obs/obs-plugins/rtmp-services/*.json
%dir %{_datadir}/obs/obs-plugins/rtmp-services/schema
%{_datadir}/obs/obs-plugins/rtmp-services/schema/*.json
%dir %{_datadir}/obs/obs-plugins/rtmp-services/locale

%dir %{_datadir}/obs/obs-plugins/text-freetype2
%{_datadir}/obs/obs-plugins/text-freetype2/*.effect
%dir %{_datadir}/obs/obs-plugins/text-freetype2/locale

%dir %{_datadir}/obs/obs-plugins/vlc-video
%dir %{_datadir}/obs/obs-plugins/vlc-video/locale

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libobs.so
%attr(755,root,root) %{_libdir}/libobs-frontend-api.so
%attr(755,root,root) %{_libdir}/libobs-opengl.so
%attr(755,root,root) %{_libdir}/libobs-scripting.so
%{_includedir}/obs
%{_pkgconfigdir}/libobs.pc
%{_pkgconfigdir}/obs-frontend-api.pc
%{_libdir}/cmake/libobs
%{_libdir}/cmake/obs-frontend-api
