Summary:	OBS Studio - live streaming and screen recording software
Name:		obs-studio
Version:	21.0.1
Release:	1
License:	GPL v2
Group:		Applications
Source0:	https://github.com/jp9000/obs-studio/archive/%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	2dbd9d5832d070a349cd97f495d788ac
Patch0:		libobs_link.patch
URL:		https://obsproject.com/
BuildRequires:	Qt5Core-devel
BuildRequires:	Qt5Gui-devel
BuildRequires:	cmake
BuildRequires:	curl-devel
BuildRequires:	fdk-aac-devel
BuildRequires:	ffmpeg-devel
BuildRequires:	fontconfig-devel
BuildRequires:	freetype-devel
BuildRequires:	jack-audio-connection-kit-devel
BuildRequires:	jansson-devel
BuildRequires:	libv4l-devel
%ifnarch x32
BuildRequires:	luajit-devel
%endif
BuildRequires:	pulseaudio-devel
BuildRequires:	python3-devel
BuildRequires:	qt5-build
BuildRequires:	qt5-qmake
BuildRequires:	swig-python
BuildRequires:	udev-devel
BuildRequires:	vlc-devel
BuildRequires:	xorg-lib-libXcomposite-devel
BuildRequires:	xorg-lib-libXinerama-devel
BuildRequires:	xorg-lib-libXrandr-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_noautoprovfiles	%{_libdir}/obs-plugins

%description
OBS Studio is software designed for capturing, compositing, encoding,
recording, and streaming video content, efficiently.

%package devel
Summary:	Header files for OBS Studio
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki %{name}
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header files for %{name} library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki %{name}.

%prep
%setup -q

%patch0 -p1

%build
install -d build
cd build

%if "%{_lib}" == "lib64"
export OBS_MULTIARCH_SUFFIX=64
%endif
%if "%{_lib}" == "libx32"
export OBS_MULTIARCH_SUFFIX=x32
%endif

%cmake \
	-DOBS_VERSION_OVERRIDE=%{version} \
		../
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
%{__make} -C build install/fast \
        DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS README.rst
%attr(755,root,root) %{_bindir}/obs
%attr(755,root,root) %{_libdir}/libobs-frontend-api.so.0.*
%ghost %{_libdir}/libobs-frontend-api.so.0
%attr(755,root,root) %{_libdir}/libobs-opengl.so.0.*
%ghost %{_libdir}/libobs-opengl.so.0
%attr(755,root,root) %{_libdir}/libobs.so.0
%attr(755,root,root) %{_libdir}/libobsglad.so.0
%attr(755,root,root) %{_libdir}/libobs-scripting.so
%dir %{_libdir}/obs-plugins
%attr(755,root,root) %{_libdir}/obs-plugins/*.so
%dir %{_libdir}/obs-scripting
%ifnarch x32
%attr(755,root,root) %{_libdir}/obs-scripting/obslua.so
%endif
%attr(755,root,root) %{_libdir}/obs-scripting/_obspython.so
%attr(755,root,root) %{_libdir}/obs-scripting/obspython.py
%{_desktopdir}/obs.desktop
%{_iconsdir}/*/*/apps/obs.png

%dir %{_datadir}/obs
%{_datadir}/obs/libobs
%{_datadir}/obs/obs-studio
%dir %{_datadir}/obs/obs-plugins

%dir %{_datadir}/obs/obs-plugins/frontend-tools
%{_datadir}/obs/obs-plugins/frontend-tools/locale
%dir %{_datadir}/obs/obs-plugins/frontend-tools/scripts
%{_datadir}/obs/obs-plugins/frontend-tools/scripts/*.lua
%{_datadir}/obs/obs-plugins/frontend-tools/scripts/*.py
%{_datadir}/obs/obs-plugins/frontend-tools/scripts/clock-source

%dir %{_datadir}/obs/obs-plugins/image-source
%{_datadir}/obs/obs-plugins/image-source/locale

%dir %{_datadir}/obs/obs-plugins/linux-alsa
%{_datadir}/obs/obs-plugins/linux-alsa/locale

%dir %{_datadir}/obs/obs-plugins/linux-capture
%{_datadir}/obs/obs-plugins/linux-capture/locale

%dir %{_datadir}/obs/obs-plugins/linux-decklink
%{_datadir}/obs/obs-plugins/linux-decklink/locale

%dir %{_datadir}/obs/obs-plugins/linux-jack
%{_datadir}/obs/obs-plugins/linux-jack/locale

%dir %{_datadir}/obs/obs-plugins/linux-pulseaudio
%{_datadir}/obs/obs-plugins/linux-pulseaudio/locale

%dir %{_datadir}/obs/obs-plugins/linux-v4l2
%{_datadir}/obs/obs-plugins/linux-v4l2/locale

%dir %{_datadir}/obs/obs-plugins/obs-ffmpeg
%{_datadir}/obs/obs-plugins/obs-ffmpeg/locale
%attr(755,root,root) %{_datadir}/obs/obs-plugins/obs-ffmpeg/ffmpeg-mux

%dir %{_datadir}/obs/obs-plugins/obs-filters
%{_datadir}/obs/obs-plugins/obs-filters/locale
%{_datadir}/obs/obs-plugins/obs-filters/*.effect
%{_datadir}/obs/obs-plugins/obs-filters/LUTs

%dir %{_datadir}/obs/obs-plugins/obs-libfdk
%{_datadir}/obs/obs-plugins/obs-libfdk/locale

%dir %{_datadir}/obs/obs-plugins/obs-outputs
%{_datadir}/obs/obs-plugins/obs-outputs/locale

%dir %{_datadir}/obs/obs-plugins/obs-transitions
%{_datadir}/obs/obs-plugins/obs-transitions/locale
%{_datadir}/obs/obs-plugins/obs-transitions/*.effect
%{_datadir}/obs/obs-plugins/obs-transitions/*.inc
%{_datadir}/obs/obs-plugins/obs-transitions/luma_wipes

%dir %{_datadir}/obs/obs-plugins/obs-x264
%{_datadir}/obs/obs-plugins/obs-x264/locale

%dir %{_datadir}/obs/obs-plugins/rtmp-services
%{_datadir}/obs/obs-plugins/rtmp-services/locale
%{_datadir}/obs/obs-plugins/rtmp-services/*.json

%dir %{_datadir}/obs/obs-plugins/text-freetype2
%{_datadir}/obs/obs-plugins/text-freetype2/locale
%{_datadir}/obs/obs-plugins/text-freetype2/*.effect

%dir %{_datadir}/obs/obs-plugins/vlc-video
%{_datadir}/obs/obs-plugins/vlc-video/locale

%files devel
%defattr(644,root,root,755)
%{_includedir}/obs
%{_libdir}/cmake/LibObs
%{_libdir}/libobs-frontend-api.so
%{_libdir}/libobs-opengl.so
%{_libdir}/libobs.so
%{_libdir}/libobsglad.so
