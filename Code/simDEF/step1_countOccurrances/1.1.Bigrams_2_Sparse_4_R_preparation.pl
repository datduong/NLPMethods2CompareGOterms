# This code prepares bigram matrix from the MEDLIBE Abstracts (Please read the read-me file before use!)
use IO::File;

my $r = IO::File->new("../../Extra/bigramWords","r") or die "Can not open file to read from;\nYou need to download 'bigramWords.gz' file from the MEDLINE Baseline Repository (NIH) website,\nand then extract it in the 'Extra' folder\n";
open(my $w1, '>', "../../Extra/Pre_Bigram_Matrix.dat") or die "Could not open file to write in\n";
open(my $w2, '>', "../../Extra/word_index.dat") or die "Could not open file to write in\n";

my $stopregex;
open (STP , "../../Extra/Stoplist.dat") or die "Can not open stoplist\n";
	$stopregex  = "(";
	while(<STP>) {
		chomp;
		if($_ ne ""){
			$_=~s/\///g;
			$stopregex .= "$_|";
		}
	}   
chop $stopregex; $stopregex .= ")";
close STP;	

my $total = 0;
my $i = 1;
my %index;
while (<$r>) {
	chomp;
	$_=~s/\|/ /g;
	my @a = split " " , $_;
	
	if(($a[1]=~$stopregex) or ($a[2]=~$stopregex)){next;}
	
	$total += $a[0];
	if (!(exists $index{$a[1]})){
		$index{$a[1]} = $i;
		$i++;
	}	

	if (!(exists $index{$a[2]})){
		$index{$a[2]} = $i;
		$i++;
	}
	
	$w1->print("$index{$a[1]} $index{$a[2]} $a[0]\n");
}

$w2->print("$total\n");
foreach (sort { $index{$a} <=> $index{$b} } keys %index){
	$w2->print("$_ $index{$_}\n");
}
