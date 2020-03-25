#!/usr/bin/perl

use 5.010;
use strict;
use warnings;
use Encode;
use charnames ':full';
use Unicode::UCD;
use List::MoreUtils qw(uniq);
use utf8;

print "create table kanji (kanji text key, meanings text, onyomi text, kunyomi text, freq integer, grade integer, jlpt integer);\n";
print "create index kanjikanji on kanji (kanji);\n";

while (<>) {
  chomp;
  my $text = decode('euc-jp', $_);
  if (/^#/) {
    next;
  }
  my @meanings = ();
  while ($text =~ /^(.*)\s+\{([^}]+)\}\s*$/) {
    $text = $1;
    my $word = $2;
    push @meanings, $word;
#    print STDERR $word, "\n";
  }
  my @attrs = split(/ /, $text);
  
  my $kanji = shift @attrs;
  shift @attrs;
  my $unicode = shift @attrs;

  if (substr($unicode, 0, 1) ne "U") {
    die "Unicode attr not in third column: $kanji";
  }
  if (hex(substr($unicode, 1)) != ord($kanji)) {
    die "Unicode doesn't match character: $kanji";
  }
  
  my $namereading_enabled = 0;
  my @onyomi = ();
  my @kunyomi = ();
  my $freq;
  my $jlpt;
  my $grade;
  for my $attr (@attrs) {
    my $type = substr($attr, 0, 1);
    my $script = Unicode::UCD::charscript(ord($type));
    if ($attr =~ /^F(\d+)$/) {
      $freq = $1;
    } elsif ($attr =~ /^G(\d+)$/) {
      $grade = $1;
    } elsif ($attr =~ /^J(\d+)$/) {
      $jlpt = $1;
    } elsif (index("BCSHFPKLIQXNVDOMEYWZ", $type) != -1) {
      
    } elsif ($attr =~ /^-?[.\p{Hiragana}]+-?$/) {
      if (not $namereading_enabled) {
        push @kunyomi, $attr;
      }
    } elsif ($attr =~ /^-?[\p{Katakana}ー]+$/) {
      if (not $namereading_enabled) {
        push @onyomi, $attr;
      }
    } elsif ($attr eq "T1") {
      $namereading_enabled = 1;
    } elsif ($attr eq "T2") {
      $namereading_enabled = 1;
    } else {
      my @scripts = uniq(map {Unicode::UCD::charscript(ord($_))} split(//, $attr));
      my $scripts = join(", ", @scripts);
      
      die "Unknown attribute $attr(scripts: $scripts) for kanji $unicode";
    }
  }

#  print encode('utf8', $text), "\n";
  my $meanings = join("\t", @meanings);
  $meanings =~ s/\'/\'\'/g;
  my $onyomi = join(" ", @onyomi);
  my $kunyomi = join(" ", @kunyomi);
  my $freq_sql = (defined $freq) ? $freq : "NULL";
  my $grade_sql = (defined $grade) ? $grade : "NULL";
  my $jlpt_sql = (defined $jlpt) ? $jlpt : "NULL";
  print encode('utf8', "insert into kanji (kanji, meanings, onyomi, kunyomi, freq, grade, jlpt) values ('$kanji', '$meanings', '$onyomi', '$kunyomi', $freq_sql, $grade_sql, $jlpt_sql);\n");

}
