
%define oname	xine-lib
%define branch	1.2
%define name	%{oname}%{branch}
# version.sh
%define version 1.2.0
%define rel	1

# bcond_without: default enabled
# bcond_with: default disabled
%bcond_with	plf

%define major	2
%define libname	%mklibname xine %major
%define devname	%mklibname -d xine %branch

%define plugin_api	%{major}.0

%if %with plf
%define distsuffix	plf
%if %mdvver >= 201100
# make EVR of plf build higher than regular to allow update, needed with rpm5 mkrel
%define extrarelsuffix plf
%endif
%endif

Summary:	A free multimedia engine (development version)
Name:		%{name}
Version:	%{version}
Release:	%mkrel %rel%{?extrarelsuffix}
License:	GPLv2+
URL:		http://xine-project.org/
Source:		http://downloads.sourceforge.net/xine/%{oname}-%{version}.tar.xz
Group:		System/Libraries
BuildRoot:	%{_tmppath}/%{name}-root
BuildRequires:	zlib-devel
BuildRequires:	freetype2-devel
BuildRequires:	fontconfig-devel
BuildRequires:	libx11-devel
BuildRequires:	libxext-devel
BuildRequires:	libxv-devel
BuildRequires:	libalsa-devel
BuildRequires:	jackit-devel
BuildRequires:	pulseaudio-devel
BuildRequires:	esound-devel
BuildRequires:	a52dec-devel
BuildRequires:	ffmpeg-devel
BuildRequires:	libgdk_pixbuf2.0-devel
BuildRequires:	imagemagick-devel
BuildRequires:	libmad-devel
BuildRequires:	libmodplug-devel
BuildRequires:	libmpcdec-devel
BuildRequires:	mng-devel
BuildRequires:	speex-devel
BuildRequires:	libtheora-devel
BuildRequires:	libvorbis-devel
BuildRequires:	gnome-vfs2-devel
BuildRequires:	libsmbclient-devel
BuildRequires:	libcdio-devel
BuildRequires:	libvcd-devel
BuildRequires:	lirc-devel
BuildRequires:	aalib-devel
BuildRequires:	libcaca-devel
BuildRequires:	directfb-devel
BuildRequires:	mesagl-devel
BuildRequires:	mesaglu-devel
BuildRequires:	SDL-devel
BuildRequires:	xcb-devel
BuildRequires:	libxinerama-devel
BuildRequires:	libxvmc-devel
BuildRequires:	vdpau-devel
BuildRequires:	libflac-devel
BuildRequires:	libv4l-devel
BuildRequires:	xmlto
BuildRequires:	librsvg
BuildRequires:	optipng
BuildRequires:	gettext-devel
BuildRequires:	docbook-dtd44-xml
%if %{mdkversion} >= 201000
BuildRequires:	xdg-basedir-devel
%endif
%if %with plf
BuildRequires:	libfaad2-devel
BuildRequires:	libdca-devel
BuildRequires:	libfame-devel
%endif

%description
Xine-lib is a free multimedia engine.

This is the development version of xine-lib.
%if %with plf
This package is in PLF because this build depends on other PLF
packages.
%endif

%package -n xine%{branch}-common
Summary:	Common files of xine-lib1.2
Group:		System/Libraries

%description -n xine%{branch}-common
Common files for xine-lib1.2, the development version of the
free multimedia engine.

%package -n %{libname}
Summary:	Shared libraries of xine-lib1.2
Group:		System/Libraries
Provides:	%{libname}-plugin-api = %{plugin_api}
Requires:	xine%{branch}-common >= %{version}

%description -n %{libname}
Shared libraries for xine-lib1.2, the development version of the
free multimedia engine.

%package -n %{devname}
Summary:	Development files for xine-lib1.2 (unstable version)
Group:		Development/C
Requires:	%{libname} = %{version}
Provides:	xine1.2-devel = %{version}-%{release}
Conflicts:	libxine-devel

%description -n %{devname}
Development libraries and headers for xine-lib1.2, the unstable version
of the free multimedia engine.

%prep
%setup -q -n %{oname}-%{version}
%apply_patches

%build
./autogen.sh noconfig
%configure2_5x \
	--with-w32-path=%{_libdir}/codecs \
	--enable-directfb \
%if %without plf
	--disable-faad
%endif

%make

%install
rm -rf %{buildroot} installed-docs
%makeinstall_std
%multiarch_binaries %{buildroot}%{_bindir}/xine-config

mv %{buildroot}%{_mandir}/man5/xine{,-%{branch}}.5
rm -f %{buildroot}%{_libdir}/*.la
mv %{buildroot}%{_datadir}/doc/xine-lib installed-docs

%find_lang libxine%{major}

%clean
rm -rf %{buildroot}

%files -n xine%{branch}-common -f libxine%{major}.lang
%defattr(-,root,root)
%doc CREDITS NEWS doc/README* doc/faq/faq.txt
# this tool lists currently supported formats (i.e. output depends on
# installed plugins); it is thus architecture-specific, but it would not
# be easy to handle it correctly, i.e. so that 32-bit calls to it return
# 32-bit plugins and 64-bit calls the 64-bit plugins; multiarch-utils is
# not used for non-devel packages -Anssi 01/2010
%{_bindir}/xine-list-%{branch}
%{_mandir}/man1/xine-list-%{branch}.1*
%{_mandir}/man5/xine-%{branch}.5*
# these should preferably be in an unversioned directory,
# but they don't conflict with main xine-lib so it is not
# critical:
%dir %{_datadir}/xine-lib
%dir %{_datadir}/xine-lib/fonts
%{_datadir}/xine-lib/fonts/*.xinefont.gz

%files -n %{libname}
%defattr(-,root,root)
%{_libdir}/libxine.so.%{major}*
%dir %{_libdir}/xine
%dir %{_libdir}/xine/plugins
%dir %{_libdir}/xine/plugins/%{plugin_api}
%dir %{_libdir}/xine/plugins/%{plugin_api}/post
%{_libdir}/xine/plugins/%{plugin_api}/mime.types
%{_libdir}/xine/plugins/%{plugin_api}/post/xineplug_post_audio_filters.so
%{_libdir}/xine/plugins/%{plugin_api}/post/xineplug_post_goom.so
%{_libdir}/xine/plugins/%{plugin_api}/post/xineplug_post_mosaico.so
%{_libdir}/xine/plugins/%{plugin_api}/post/xineplug_post_planar.so
%{_libdir}/xine/plugins/%{plugin_api}/post/xineplug_post_switch.so
%{_libdir}/xine/plugins/%{plugin_api}/post/xineplug_post_tvtime.so
%{_libdir}/xine/plugins/%{plugin_api}/post/xineplug_post_visualizations.so
%{_libdir}/xine/plugins/%{plugin_api}/xineplug_ao_out_alsa.so
%{_libdir}/xine/plugins/%{plugin_api}/xineplug_ao_out_esd.so
%{_libdir}/xine/plugins/%{plugin_api}/xineplug_ao_out_file.so
%{_libdir}/xine/plugins/%{plugin_api}/xineplug_ao_out_jack.so
%{_libdir}/xine/plugins/%{plugin_api}/xineplug_ao_out_none.so
%{_libdir}/xine/plugins/%{plugin_api}/xineplug_ao_out_oss.so
%{_libdir}/xine/plugins/%{plugin_api}/xineplug_ao_out_pulseaudio.so
%{_libdir}/xine/plugins/%{plugin_api}/xineplug_decode_a52.so
%{_libdir}/xine/plugins/%{plugin_api}/xineplug_decode_bitplane.so
%{_libdir}/xine/plugins/%{plugin_api}/xineplug_decode_dts.so
%{_libdir}/xine/plugins/%{plugin_api}/xineplug_decode_dvaudio.so
%{_libdir}/xine/plugins/%{plugin_api}/xineplug_decode_dxr3_spu.so
%{_libdir}/xine/plugins/%{plugin_api}/xineplug_decode_dxr3_video.so
%if %with plf
%{_libdir}/xine/plugins/%{plugin_api}/xineplug_decode_faad.so
%endif
%{_libdir}/xine/plugins/%{plugin_api}/xineplug_decode_ff.so
%{_libdir}/xine/plugins/%{plugin_api}/xineplug_decode_gdk_pixbuf.so
%{_libdir}/xine/plugins/%{plugin_api}/xineplug_decode_gsm610.so
%{_libdir}/xine/plugins/%{plugin_api}/xineplug_decode_image.so
%{_libdir}/xine/plugins/%{plugin_api}/xineplug_decode_lpcm.so
%{_libdir}/xine/plugins/%{plugin_api}/xineplug_decode_mad.so
%{_libdir}/xine/plugins/%{plugin_api}/xineplug_decode_mpc.so
%{_libdir}/xine/plugins/%{plugin_api}/xineplug_decode_mpeg2.so
%{_libdir}/xine/plugins/%{plugin_api}/xineplug_decode_real.so
%{_libdir}/xine/plugins/%{plugin_api}/xineplug_decode_rgb.so
%{_libdir}/xine/plugins/%{plugin_api}/xineplug_decode_spu.so
%{_libdir}/xine/plugins/%{plugin_api}/xineplug_decode_spucc.so
%{_libdir}/xine/plugins/%{plugin_api}/xineplug_decode_spucmml.so
%{_libdir}/xine/plugins/%{plugin_api}/xineplug_decode_spudvb.so
%{_libdir}/xine/plugins/%{plugin_api}/xineplug_decode_spuhdmv.so
%{_libdir}/xine/plugins/%{plugin_api}/xineplug_decode_vdpau_h264.so
%{_libdir}/xine/plugins/%{plugin_api}/xineplug_decode_vdpau_h264_alter.so
%{_libdir}/xine/plugins/%{plugin_api}/xineplug_decode_vdpau_mpeg12.so
%{_libdir}/xine/plugins/%{plugin_api}/xineplug_decode_vdpau_mpeg4.so
%{_libdir}/xine/plugins/%{plugin_api}/xineplug_decode_vdpau_vc1.so
%{_libdir}/xine/plugins/%{plugin_api}/xineplug_decode_yuv.so
%{_libdir}/xine/plugins/%{plugin_api}/xineplug_dmx_asf.so
%{_libdir}/xine/plugins/%{plugin_api}/xineplug_dmx_audio.so
%{_libdir}/xine/plugins/%{plugin_api}/xineplug_dmx_avi.so
%{_libdir}/xine/plugins/%{plugin_api}/xineplug_dmx_fli.so
%{_libdir}/xine/plugins/%{plugin_api}/xineplug_dmx_flv.so
%{_libdir}/xine/plugins/%{plugin_api}/xineplug_dmx_games.so
%{_libdir}/xine/plugins/%{plugin_api}/xineplug_dmx_iff.so
%{_libdir}/xine/plugins/%{plugin_api}/xineplug_dmx_image.so
%{_libdir}/xine/plugins/%{plugin_api}/xineplug_dmx_matroska.so
%{_libdir}/xine/plugins/%{plugin_api}/xineplug_dmx_mng.so
%{_libdir}/xine/plugins/%{plugin_api}/xineplug_dmx_modplug.so
%{_libdir}/xine/plugins/%{plugin_api}/xineplug_dmx_mpeg.so
%{_libdir}/xine/plugins/%{plugin_api}/xineplug_dmx_mpeg_block.so
%{_libdir}/xine/plugins/%{plugin_api}/xineplug_dmx_mpeg_elem.so
%{_libdir}/xine/plugins/%{plugin_api}/xineplug_dmx_mpeg_pes.so
%{_libdir}/xine/plugins/%{plugin_api}/xineplug_dmx_mpeg_ts.so
%{_libdir}/xine/plugins/%{plugin_api}/xineplug_dmx_nsv.so
%{_libdir}/xine/plugins/%{plugin_api}/xineplug_dmx_playlist.so
%{_libdir}/xine/plugins/%{plugin_api}/xineplug_dmx_pva.so
%{_libdir}/xine/plugins/%{plugin_api}/xineplug_dmx_qt.so
%{_libdir}/xine/plugins/%{plugin_api}/xineplug_dmx_rawdv.so
%{_libdir}/xine/plugins/%{plugin_api}/xineplug_dmx_real.so
%{_libdir}/xine/plugins/%{plugin_api}/xineplug_dmx_slave.so
%{_libdir}/xine/plugins/%{plugin_api}/xineplug_dmx_vc1_es.so
%{_libdir}/xine/plugins/%{plugin_api}/xineplug_dmx_yuv4mpeg2.so
%{_libdir}/xine/plugins/%{plugin_api}/xineplug_dmx_yuv_frames.so
%{_libdir}/xine/plugins/%{plugin_api}/xineplug_flac.so
%{_libdir}/xine/plugins/%{plugin_api}/xineplug_inp_cdda.so
%{_libdir}/xine/plugins/%{plugin_api}/xineplug_inp_dvb.so
%{_libdir}/xine/plugins/%{plugin_api}/xineplug_inp_dvd.so
%{_libdir}/xine/plugins/%{plugin_api}/xineplug_inp_file.so
%{_libdir}/xine/plugins/%{plugin_api}/xineplug_inp_gnome_vfs.so
%{_libdir}/xine/plugins/%{plugin_api}/xineplug_inp_http.so
%{_libdir}/xine/plugins/%{plugin_api}/xineplug_inp_mms.so
%{_libdir}/xine/plugins/%{plugin_api}/xineplug_inp_net.so
%{_libdir}/xine/plugins/%{plugin_api}/xineplug_inp_pnm.so
%{_libdir}/xine/plugins/%{plugin_api}/xineplug_inp_pvr.so
%{_libdir}/xine/plugins/%{plugin_api}/xineplug_inp_rtp.so
%{_libdir}/xine/plugins/%{plugin_api}/xineplug_inp_rtsp.so
%{_libdir}/xine/plugins/%{plugin_api}/xineplug_inp_smb.so
%{_libdir}/xine/plugins/%{plugin_api}/xineplug_inp_stdin_fifo.so
%{_libdir}/xine/plugins/%{plugin_api}/xineplug_inp_v4l2.so
%{_libdir}/xine/plugins/%{plugin_api}/xineplug_inp_vcd.so
%{_libdir}/xine/plugins/%{plugin_api}/xineplug_inp_vcdo.so
%{_libdir}/xine/plugins/%{plugin_api}/xineplug_nsf.so
%{_libdir}/xine/plugins/%{plugin_api}/xineplug_sputext.so
%{_libdir}/xine/plugins/%{plugin_api}/xineplug_vdr.so
%{_libdir}/xine/plugins/%{plugin_api}/xineplug_vo_out_aa.so
%{_libdir}/xine/plugins/%{plugin_api}/xineplug_vo_out_caca.so
%{_libdir}/xine/plugins/%{plugin_api}/xineplug_vo_out_directfb.so
%{_libdir}/xine/plugins/%{plugin_api}/xineplug_vo_out_dxr3.so
%{_libdir}/xine/plugins/%{plugin_api}/xineplug_vo_out_fb.so
%{_libdir}/xine/plugins/%{plugin_api}/xineplug_vo_out_none.so
%{_libdir}/xine/plugins/%{plugin_api}/xineplug_vo_out_opengl.so
%{_libdir}/xine/plugins/%{plugin_api}/xineplug_vo_out_raw.so
%{_libdir}/xine/plugins/%{plugin_api}/xineplug_vo_out_sdl.so
%{_libdir}/xine/plugins/%{plugin_api}/xineplug_vo_out_vdpau.so
%{_libdir}/xine/plugins/%{plugin_api}/xineplug_vo_out_xcbshm.so
%{_libdir}/xine/plugins/%{plugin_api}/xineplug_vo_out_xcbxv.so
%{_libdir}/xine/plugins/%{plugin_api}/xineplug_vo_out_xdirectfb.so
%{_libdir}/xine/plugins/%{plugin_api}/xineplug_vo_out_xshm.so
%{_libdir}/xine/plugins/%{plugin_api}/xineplug_vo_out_xv.so
%{_libdir}/xine/plugins/%{plugin_api}/xineplug_vo_out_xvmc.so
%{_libdir}/xine/plugins/%{plugin_api}/xineplug_vo_out_xxmc.so
%{_libdir}/xine/plugins/%{plugin_api}/xineplug_xiph.so
%ifarch %ix86
%dir %{_libdir}/xine/plugins/%{plugin_api}/vidix
%{_libdir}/xine/plugins/%{plugin_api}/vidix/*_vid.so
%{_libdir}/xine/plugins/%{plugin_api}/xineplug_decode_qt.so
%{_libdir}/xine/plugins/%{plugin_api}/xineplug_decode_w32dll.so
%{_libdir}/xine/plugins/%{plugin_api}/xineplug_vo_out_vidix.so
%endif

%files -n %{devname}
%defattr(-,root,root)
%doc installed-docs/*
%{_bindir}/xine-config
%{multiarch_bindir}/xine-config
%{_includedir}/xine.h
%{_includedir}/xine
%{_datadir}/aclocal/xine.m4
%{_libdir}/libxine.so
%{_libdir}/pkgconfig/libxine.pc
%{_mandir}/man1/xine-config.1*
